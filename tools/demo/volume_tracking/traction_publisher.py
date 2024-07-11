import datetime
import logging
import os

from lab_share_lib.config.rabbit_server_details import RabbitServerDetails
from lab_share_lib.constants import RABBITMQ_HEADER_VALUE_ENCODER_TYPE_JSON
from lab_share_lib.rabbit.avro_encoder import AvroEncoderJson
from lab_share_lib.rabbit.basic_publisher import BasicPublisher
from lab_share_lib.rabbit.schema_registry import SchemaRegistry

REDPANDA_URL = os.getenv("REDPANDA_URL", "http://localhost:8081")
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_PORT = os.getenv("RABBITMQ_PORT", "5672")
RABBITMQ_USERNAME = os.getenv("RABBITMQ_USERNAME", "admin")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD", "development")
RABBITMQ_VHOST = os.getenv("RABBITMQ_VHOST", "tol")
RABBITMQ_EXCHANGE = os.getenv("RABBITMQ_EXCHANGE", "traction")
SCHEMA_SUBJECT = "create-aliquot-in-mlwh"

logger = logging.getLogger(__name__)


def build_traction_volume_tracking_message():
    return {
        "limsId": "Traction",
        "messageCreateDateUtc": datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "messageUuid": "4b6b9444-8935-4376-929d-06dae7b775f3",
        "recordedAt": datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "volume": 1.5,
        "concentration": 10.0,
        "insertSize": 100,
        "aliquotType": "primary",
        "limsUuid": "4b6b9444-8935-4376-929d-06dae7b77523",
        "sourceType": "library",
        "sourceBarcode": "TRAC-2-1572",
        "sampleName": "SAMPLENAME",
        "usedByBarcode": "SQPD-1212",
        "usedByType": "none",
    }


if __name__ == "__main__":
    rmq_details = RabbitServerDetails(
        uses_ssl=False,
        host=RABBITMQ_HOST,
        port=RABBITMQ_PORT,
        username=RABBITMQ_USERNAME,
        password=RABBITMQ_PASSWORD,
        vhost=RABBITMQ_VHOST,
    )

    publisher = BasicPublisher(rmq_details, publish_retry_delay=5, publish_max_retries=36, verify_cert=False)

    message = build_traction_volume_tracking_message()

    logging.info(f"Message: {message}")

    registry = SchemaRegistry(REDPANDA_URL, verify=False)
    encoder = AvroEncoderJson(registry, SCHEMA_SUBJECT)
    encoded_message = encoder.encode([message], version="latest")

    publisher.publish_message(
        exchange=RABBITMQ_EXCHANGE,
        routing_key="",
        body=encoded_message.body,
        subject=SCHEMA_SUBJECT,
        schema_version=encoded_message.version,
        encoder_type=RABBITMQ_HEADER_VALUE_ENCODER_TYPE_JSON,
    )
