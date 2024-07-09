import json
import os
import argparse

from lab_share_lib.config.rabbit_server_details import RabbitServerDetails
from lab_share_lib.rabbit.basic_publisher import BasicPublisher

from tools.demo.create_aliquot_in_mlwh_messages import build_create_aliquot_message

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_PORT = os.getenv("RABBITMQ_PORT", "5671")
RABBITMQ_USERNAME = os.getenv("RABBITMQ_USERNAME", "psd")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD", "psd")
RABBITMQ_VHOST = os.getenv("RABBITMQ_VHOST", "test")
RABBITMQ_EXCHANGE = os.getenv("RABBITMQ_EXCHANGE", "psd.tol-lab-share")
RABBITMQ_ROUTING_KEY = os.getenv("RABBITMQ_ROUTING_KEY", "development.saved.aliquots.*")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="TOL LabShare message publisher demo script.")
    parser.add_argument(
        "--routing_key", default="development.saved.aliquots.1", help="Routing key for the binding"
    )

    args = parser.parse_args()

    rmq_details = RabbitServerDetails(
        uses_ssl=False,
        host=RABBITMQ_HOST,
        port=RABBITMQ_PORT,
        username=RABBITMQ_USERNAME,
        password=RABBITMQ_PASSWORD,
        vhost=RABBITMQ_VHOST
    )

    publisher = BasicPublisher(
        rmq_details,
        publish_retry_delay=5,
        publish_max_retries=36,
        verify_cert=False
    )

    message = build_create_aliquot_message()
    publisher.publish_message(
        exchange=RABBITMQ_EXCHANGE,
        routing_key=args.routing_key,
        body=json.dumps(message),
        subject=None,
        schema_version=None,
        encoder_type=None,
    )
    





