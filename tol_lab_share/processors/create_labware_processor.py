import logging

from lab_share_lib.processing.rabbit_message import RabbitMessage

from tol_lab_share.messages.output_feedback_message import OutputFeedbackMessage
from tol_lab_share.messages.input_create_labware_message import InputCreateLabwareMessage
from tol_lab_share.messages.output_traction_message import OutputTractionMessage

from tol_lab_share.data_resolvers.data_resolver import DataResolver


logger = logging.getLogger(__name__)


class CreateLabwareProcessor:
    def __init__(self, schema_registry, basic_publisher, config):
        logger.debug("CreateLabwareProcessor::__init__")

        self._basic_publisher = basic_publisher
        self._schema_registry = schema_registry
        self._config = config

    def process(self, message: RabbitMessage) -> bool:
        logger.debug("CreateLabwareProcessor::process")
        logger.debug(f"Received: { message.message }")

        input = DataResolver(InputCreateLabwareMessage(message))
        if input.validate():
            input.resolve()

        output_feedback_message = OutputFeedbackMessage()
        input.add_to_feedback_message(output_feedback_message)

        if output_feedback_message.validate():
            output_traction_message = OutputTractionMessage()
            input.add_to_traction_message(output_traction_message)

            if output_traction_message.validate():
                output_traction_message.send(url=self._config.TRACTION_URL)

            output_traction_message.add_to_feedback_message(output_feedback_message)

        output_feedback_message.publish(
            publisher=self._basic_publisher,
            schema_registry=self._schema_registry,
            exchange=self._config.RABBITMQ_FEEDBACK_EXCHANGE,
        )

        return output_feedback_message.operation_was_error_free is True
