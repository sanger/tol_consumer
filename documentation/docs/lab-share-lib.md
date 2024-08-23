# lab-share-lib

`lab-share-lib` is a separate [library](https://github.com/sanger/lab-share-lib) that encapsulates AMQP connectivity logic, message deserialization and schema validation. Sections below are some discussions on how it encapsulates logic related to messaging infrastructure and schema validation.

## Connectivity with Message Queues

`tol-lab-share` establishes AMQP connections with a RabbitMQ broker. `lab-share-lib`, therefore, uses [`pika`](https://pika.readthedocs.io/en/stable/) library to manage connectivity logic and handle failures. `pika` uses several callback functions to handle messaging logic, and these are captured in [`lab_share_lib/rabbit/async_consumer.py`](https://github.com/sanger/lab-share-lib/blob/6724ec3c5053b75bb2a33958621930d9bb876a31/lab_share_lib/rabbit/async_consumer.py) in `lab-share-lib`.

```python linenums="1" title="Snippets on connectivity logic and callbacks with RabbitMQ broker"

def start_consuming(self):
    if self._channel:
        LOGGER.info("Issuing consumer related RPC commands")
        self.add_on_cancel_callback()
        self._consumer_tag = self._channel.basic_consume(self._queue, self.on_message)
        self.was_consuming = True
        self.had_transient_error = False
        self._consuming = True

def on_message(self, channel, basic_deliver, properties, body):
    LOGGER.info(f"Received message # {basic_deliver.delivery_tag}")
    MESSAGE_LOGGER.info(f"Received message # {basic_deliver.delivery_tag} with body:  {body}")
    delivery_tag = basic_deliver.delivery_tag

    try:
        should_ack_message = self._process_message(properties.headers, body)
    except TransientRabbitError:
        self.had_transient_error = True
        raise

    if should_ack_message:
        LOGGER.info("Acknowledging message # %s", delivery_tag)
        channel.basic_ack(delivery_tag)
    else:
        LOGGER.info("Rejecting message # %s", delivery_tag)
        channel.basic_nack(delivery_tag, requeue=False)
```

`AsyncConsumer` is a class declared in `lab-share-lib` that contains all these logic related to AMQP connectivity. `AsyncConsumer` is instantiated in a `BackgroundConsumer` thread, that is started when `tol-lab-share` is run at [main.py](https://github.com/sanger/tol-lab-share/blob/dce2e4441313791171922caaec8450e238a1e939/main.py).

!!! note

    Note that `AsyncConsumer` is instantiated at the overridden function`run` in `BackgroundConsumer`, and each `AsyncConsumer` listens to a certain queue. In `bring_stack_up` function at [`rabbit_stack.py`](https://github.com/sanger/lab-share-lib/blob/bef1588724a9449f1a33b78dbcc60160d77df129/lab_share_lib/rabbit/rabbit_stack.py), `BackgroundConsumer` objects are created, and the `run` function is invoked by calling `start()` method on the consumer thread. When `on_message` callback is triggered when a message is received to the queue, the `process_message` function which was handed over to the `BackgroundConsumer` class (and therefore `AsyncConsumer` class) is invoked.


## Message Processors

For each message type identified by the `subject`, processor objects that inherits from `BaseProcessor` are instantiated. When a message is received with a certain subject in the message header from the queue, that message is processed by the corresponding processor.

!!! note

    A subject-to-processor mapping is declared through the class `RabbitConfig`. This is declared in `tol_lab_share/config/rabbit.py` and can **not** be updated dynamically through deployment configurations.

    ```py linenums="1" title="rabbit.py"
    RABBITMQ_SERVERS = [
        RabbitConfig(
            consumer_details=TOL_RABBIT_SERVER,
            consumed_queue="tol.crud-operations",
            message_subjects={
                RABBITMQ_SUBJECT_CREATE_LABWARE: MessageSubjectConfig(
                    processor=CreateLabwareProcessor, reader_schema_version="2"
                ),
                RABBITMQ_SUBJECT_UPDATE_LABWARE: MessageSubjectConfig(
                    processor=UpdateLabwareProcessor, reader_schema_version="1"
                ),
            },
            publisher_details=TOL_RABBIT_SERVER,
        ),
        RabbitConfig(
            consumer_details=ISG_RABBIT_SERVER,
            consumed_queue="tls.poolxp-export-to-traction",
            message_subjects={
                RABBITMQ_SUBJECT_BIOSCAN_POOL_XP_TO_TRACTION: MessageSubjectConfig(
                    processor=BioscanPoolXpToTractionProcessor, reader_schema_version="1"
                ),
            },
            publisher_details=ISG_RABBIT_SERVER,
        ),
        RabbitConfig(
            consumer_details=ISG_RABBIT_SERVER,
            consumed_queue="tls.volume-tracking",
            message_subjects={
                RABBITMQ_SUBJECT_CREATE_ALIQUOT_IN_MLWH: MessageSubjectConfig(
                    processor=CreateAliquotProcessor, reader_schema_version="1"
                ),
            },
            publisher_details=MLWH_RABBIT_SERVER,
        ),
    ]
    ```

    This maps the messages coming from servers to the processors based on the subjects declared in the message header.

    <center>

    | **Messaging Server** |            **Subject in the header**           |            **Processor**           |   **Published to**   |
    |:--------------------:|:----------------------------------------------:|:----------------------------------:|:--------------------:|
    | `TOL_RABBIT_SERVER`  | `RABBITMQ_SUBJECT_CREATE_LABWARE`              | `CreateLabwareProcessor`           | `TOL_RABBIT_SERVER`  |
    | `TOL_RABBIT_SERVER`  | `RABBITMQ_SUBJECT_UPDATE_LABWARE`              | `UpdateLabwareProcessor`           | `TOL_RABBIT_SERVER`  |
    | `ISG_RABBIT_SERVER`  | `RABBITMQ_SUBJECT_BIOSCAN_POOL_XP_TO_TRACTION` | `BioscanPoolXpToTractionProcessor` | `ISG_RABBIT_SERVER`  |
    | `ISG_RABBIT_SERVER`  | `RABBITMQ_SUBJECT_CREATE_ALIQUOT_IN_MLWH`      | `CreateAliquotProcessor`           | `MLWH_RABBIT_SERVER` |

    </center>

    Each server identified by `consumer_details` and `publisher_details` are declared in `rabbit_servers.py` in `tol-lab-share`. The processors that inherit from `BaseProcessor` are in `tol_lab_share/processors` package.

## Schema Registry

`lab-share-lib` uses Python `requests` library to interact with RedPanda's API. The schema responses are cached using `@lru_cache`, and will be re-fetched upon cache expiry and cache misses.
Upon arrival of messages (i.e., invocation of `on_message` callback through `pika`) the message bytes are converted into a `RabbitMessage` instance, and `decode` function is called for each instance. The `decode` function uses the cached schemas, and will validate the message against the reader and writer schema versions. Reader schema version for each message is configured in `rabbit.py` as noted above. The writer schema is encoded into the message headers, which the `decode` function extracts and uses for validation. 

!!! note

    Therefore, schema validations occur _before_ application control returns to code in `tol-lab-share`. Schema validations are done via `lab-share-lib`. However, `lab-share-lib` and `tol-lab-share` are **not** two components; `tol-lab-share` is an up and running component while `lab-share-lib` provides necessary functions that enable `tol-lab-share` to perform its tasks.


