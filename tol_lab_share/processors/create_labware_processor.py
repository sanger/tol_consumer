from lab_share_lib.rabbit.avro_encoder import AvroEncoderBinary
import logging

from tol_lab_share.constants import (
    RABBITMQ_SUBJECT_CREATE_LABWARE_FEEDBACK,
    RABBITMQ_ROUTING_KEY_CREATE_LABWARE_FEEDBACK,
)
from lab_share_lib.constants import RABBITMQ_HEADER_VALUE_ENCODER_TYPE_BINARY
from lab_share_lib.processing.rabbit_message import RabbitMessage

from tol_lab_share.messages.output_feedback_message import OutputFeedbackMessage
from tol_lab_share.messages.input_create_labware_message import InputCreateLabwareMessage

# from tol_lab_share.messages import InputCreateLabwareMessage, OutputFeedbackMessage
from tol_lab_share.data_resolvers.data_resolver import DataResolver

logger = logging.getLogger(__name__)


class CreateLabwareProcessor:
    def __init__(self, schema_registry, basic_publisher, config):
        logger.debug("CreateLabwareProcessor::__init__")
        self._encoder = AvroEncoderBinary(schema_registry, RABBITMQ_SUBJECT_CREATE_LABWARE_FEEDBACK)
        self._basic_publisher = basic_publisher
        self._config = config

    def process(self, message: RabbitMessage) -> bool:
        logger.debug("CreateLabwareProcessor::process")
        logger.debug(f"Received: { message.message }")

        input = DataResolver(InputCreateLabwareMessage(message))
        if input.validate():
            input.resolve()

        output_feedback_message = OutputFeedbackMessage()
        input.add_to_feedback_message(output_feedback_message)

        self.publish(output_feedback_message)

        return output_feedback_message.operation_was_error_free is True

    def publish(self, output_feedback_message: OutputFeedbackMessage) -> None:
        message = output_feedback_message.to_json()
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
