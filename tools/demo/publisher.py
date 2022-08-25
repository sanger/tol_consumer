import os
from lab_share_lib.rabbit.schema_registry import SchemaRegistry
from lab_share_lib.rabbit.basic_publisher import BasicPublisher
from lab_share_lib.rabbit.avro_encoder import AvroEncoderBinary
from lab_share_lib.types import RabbitServerDetails
from lab_share_lib.constants import RABBITMQ_HEADER_VALUE_ENCODER_TYPE_BINARY


from testing_data import CREATE_LABWARE_MSG, UPDATE_LABWARE_MSG

REDPANDA_URL = os.getenv("REDPANDA_URL", "http://localhost")
REDPANDA_API_KEY = os.getenv("REDPANDA_API_KEY", "test")

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_PORT = os.getenv("RABBITMQ_PORT", "5671")
RABBITMQ_USERNAME = os.getenv("RABBITMQ_USERNAME", "psd")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD", "psd")
RABBITMQ_VHOST = os.getenv("RABBITMQ_VHOST", "tol")
RABBITMQ_EXCHANGE = os.getenv("RABBITMQ_EXCHANGE", "tol-team.tol")
RABBITMQ_ROUTING_KEY = os.getenv("RABBITMQ_ROUTING_KEY", "crud.1")


def send_message(msg, subject, registry, publisher):
    print(f"Want to send { subject } message { msg }\n")

    encoder = AvroEncoderBinary(registry, subject)
    encoded_message = encoder.encode([msg], version="latest")

    print(f"Publishing message { encoded_message }\n")

    publisher.publish_message(
        RABBITMQ_EXCHANGE,
        RABBITMQ_ROUTING_KEY,
        encoded_message.body,
        subject,
        encoded_message.version,
        RABBITMQ_HEADER_VALUE_ENCODER_TYPE_BINARY,
    )


if __name__ == "__main__":
    registry = SchemaRegistry(REDPANDA_URL, REDPANDA_API_KEY, verify=False)

    rabbitmq_details = RabbitServerDetails(
        uses_ssl=True,
        host=RABBITMQ_HOST,
        port=RABBITMQ_PORT,
        username=RABBITMQ_USERNAME,
        password=RABBITMQ_PASSWORD,
        vhost=RABBITMQ_VHOST,
    )
    publisher = BasicPublisher(rabbitmq_details, publish_retry_delay=5, publish_max_retries=36, verify_cert=False)

    for _barcode in range(0, 20):

        send_message(CREATE_LABWARE_MSG, "create-labware", registry, publisher)
        send_message(UPDATE_LABWARE_MSG, "update-labware", registry, publisher)
