import os
from lab_share_lib.rabbit.schema_registry import SchemaRegistry
from lab_share_lib.rabbit.basic_publisher import BasicPublisher
from lab_share_lib.rabbit.avro_encoder import AvroEncoder
from lab_share_lib.types import  RabbitServerDetails

REDPANDA_URL=os.getenv("REDPANDA_URL", "http://localhost")
REDPANDA_API_KEY=os.getenv("REDPANDA_API_KEY", "test")
REDPANDA_SUBJECT=os.getenv("REDPANDA_SUBJECT", "create-labware")

RABBITMQ_HOST=os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_PORT=os.getenv("RABBITMQ_PORT", "5671")
RABBITMQ_USERNAME=os.getenv("RABBITMQ_USERNAME", "psd")
RABBITMQ_PASSWORD=os.getenv("RABBITMQ_PASSWORD", "psd")
RABBITMQ_VHOST=os.getenv("RABBITMQ_VHOST", "tol")
RABBITMQ_EXCHANGE=os.getenv("RABBITMQ_EXCHANGE", "tol-team.tol")
RABBITMQ_ROUTING_KEY=os.getenv("RABBITMQ_ROUTING_KEY", "crud.1")

if __name__ == "__main__":
    registry = SchemaRegistry(REDPANDA_URL, REDPANDA_API_KEY)
    encoder = AvroEncoder(registry, REDPANDA_SUBJECT)

    rabbitmq_details = RabbitServerDetails(
        uses_ssl=True,
        host=RABBITMQ_HOST,
        port=RABBITMQ_PORT,
        username=RABBITMQ_USERNAME,
        password=RABBITMQ_PASSWORD,
        vhost=RABBITMQ_VHOST,
    )
    publisher = BasicPublisher(rabbitmq_details)

    for barcode in range(1,2):
        msg = {"barcode": str(barcode), "name": "1234"}

        print(f"Publishing message { msg }\n")

        encoded_message = encoder.encode([msg])

        publisher.publish_message(
            RABBITMQ_EXCHANGE,
            RABBITMQ_ROUTING_KEY,
            encoded_message.body,
            REDPANDA_SUBJECT,
            encoded_message.version,
        )

