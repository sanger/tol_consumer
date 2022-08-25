from lab_share_lib.rabbit.avro_encoder import AvroEncoder
import logging

from tol_lab_share.constants import (
    RABBITMQ_SUBJECT_CREATE_LABWARE_FEEDBACK,
    RABBITMQ_ROUTING_KEY_CREATE_LABWARE_FEEDBACK,
)
from lab_share_lib.constants import RABBITMQ_HEADER_VALUE_ENCODER_TYPE_BINARY

from lab_share_lib.processing.rabbit_message import RabbitMessage

logger = logging.getLogger(__name__)


class CreateLabwareProcessor:
    def __init__(self, schema_registry, basic_publisher, config):
        logger.debug("CreateLabwareProcessor::__init__")
        self._encoder = AvroEncoder(schema_registry, RABBITMQ_SUBJECT_CREATE_LABWARE_FEEDBACK)
        self._basic_publisher = basic_publisher
        self._config = config

    def process(self, message: RabbitMessage) -> bool:
        logger.debug("CreateLabwareProcessor::process")
        logger.debug(f"Received: { message.message }")

        message = {
            "sourceMessageUuid": str(message.message["messageUuid"].decode("utf-8")),
            "countOfTotalSamples": len(message.message["labware"]["samples"]),
            "countOfValidSamples": len(message.message["labware"]["samples"]),
            "operationWasErrorFree": str(True),
            "errors": [],
        }

        encoded_message = self._encoder.encode([message])

        logger.debug(f"Sending: { encoded_message }")

        self._basic_publisher.publish_message(
            self._config.RABBITMQ_FEEDBACK_EXCHANGE,
            RABBITMQ_ROUTING_KEY_CREATE_LABWARE_FEEDBACK,
            encoded_message.body,
            RABBITMQ_SUBJECT_CREATE_LABWARE_FEEDBACK,
            encoded_message.version,
            RABBITMQ_HEADER_VALUE_ENCODER_TYPE_BINARY,
        )
        return True
