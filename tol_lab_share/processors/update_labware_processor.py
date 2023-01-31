from lab_share_lib.rabbit.avro_encoder import AvroEncoderBinary
import logging

from tol_lab_share.constants import (
    RABBITMQ_SUBJECT_UPDATE_LABWARE_FEEDBACK,
    RABBITMQ_ROUTING_KEY_UPDATE_LABWARE_FEEDBACK,
)
from lab_share_lib.constants import RABBITMQ_HEADER_VALUE_ENCODER_TYPE_BINARY
from lab_share_lib.processing.rabbit_message import RabbitMessage

logger = logging.getLogger(__name__)


class UpdateLabwareProcessor:
    """Class to handle consuming update-labware messages from TOL"""

    def __init__(self, schema_registry, basic_publisher, config):
        """Resets data for the processor
        Parameters:
        schema_registry (SchemaRegistry) the redpanda schema registry we will us to validate messages
        basic_publisher (BasicPublisher) instance that will provide the communication with the queues system
        config (Any) mainconfiguration from the app
        """
        logger.debug("UpdateLabwareProcessor::__init__")
        self._encoder = AvroEncoderBinary(schema_registry, RABBITMQ_SUBJECT_UPDATE_LABWARE_FEEDBACK)
        self._basic_publisher = basic_publisher
        self._config = config

    def process(self, message: RabbitMessage) -> bool:
        """Consumes a message for updating labware information. At now no relevant action is attached to
        this.
        Returns:
        bool indicating if the message was correctly consumed
        """
        logger.debug("UpdateLabwareProcessor::process")
        logger.debug(f"Received: { message.message }")

        message = {
            "sourceMessageUuid": str(message.message["messageUuid"].decode()),
            "operationWasErrorFree": str(True),
            "errors": [],
        }

        encoded_message = self._encoder.encode([message])

        logger.debug(f"Sending: { encoded_message }")

        self._basic_publisher.publish_message(
            self._config.RABBITMQ_FEEDBACK_EXCHANGE,
            RABBITMQ_ROUTING_KEY_UPDATE_LABWARE_FEEDBACK,
            encoded_message.body,
            RABBITMQ_SUBJECT_UPDATE_LABWARE_FEEDBACK,
            encoded_message.version,
            RABBITMQ_HEADER_VALUE_ENCODER_TYPE_BINARY,
        )

        return True
