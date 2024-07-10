import json
import os
import argparse
import logging
from datetime import datetime, UTC
from uuid import uuid4

from lab_share_lib.config.rabbit_server_details import RabbitServerDetails
from lab_share_lib.rabbit.basic_publisher import BasicPublisher

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_PORT = os.getenv("RABBITMQ_PORT", "5671")
RABBITMQ_USERNAME = os.getenv("RABBITMQ_USERNAME", "psd")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD", "psd")
RABBITMQ_VHOST = os.getenv("RABBITMQ_VHOST", "test")
RABBITMQ_EXCHANGE = os.getenv("RABBITMQ_EXCHANGE", "psd.tol-lab-share")
RABBITMQ_ROUTING_KEY = os.getenv("RABBITMQ_ROUTING_KEY", "development.saved.aliquots.*")

logger = logging.getLogger(__name__)


def build_create_aliquot_message():
    dt = datetime.now(UTC)
    date_string = dt.strftime("%Y-%m-%dT%H:%M:%SZ")

    return {
        "lims": "traction",
        "aliquot": {
            "id_lims": "LIMS123456",
            "lims_uuid": str(uuid4()),
            "aliquot_type": "derived",
            "source_type": "primary",
            "source_barcode": "SRC123456",
            "sample_name": "SampleA",
            "used_by_type": "Research",
            "used_by_barcode": "USR123456",
            "volume": 50.50,
            "concentration": 200.10,
            "last_updated": date_string,
            "recorded_at": date_string,
            "created_at": date_string,
            "insert_size": 350,
        },
    }


# This file is a demo script to test publishing messages to the warehouse rabbitmq.
# Note that the routing key needs to be parameterised with the message id for the wildcard (#) in
# staging.saved.aliquot.#. The environment (e.g. staging) needs to be read from a configuration file.
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TOL LabShare message publisher demo script.")
    parser.add_argument("--routing_key", default="development.saved.aliquots.1", help="Routing key for the binding")

    args = parser.parse_args()

    rmq_details = RabbitServerDetails(
        uses_ssl=False,
        host=RABBITMQ_HOST,
        port=RABBITMQ_PORT,
        username=RABBITMQ_USERNAME,
        password=RABBITMQ_PASSWORD,
        vhost=RABBITMQ_VHOST,
    )

    publisher = BasicPublisher(rmq_details, publish_retry_delay=5, publish_max_retries=36, verify_cert=False)

    message = json.dumps(build_create_aliquot_message())

    publisher.publish_message(
        exchange=RABBITMQ_EXCHANGE,
        routing_key="staging.saved.aliquot.1000",
        body=message,
        subject=None,
        schema_version=None,
        encoder_type=None,
    )
