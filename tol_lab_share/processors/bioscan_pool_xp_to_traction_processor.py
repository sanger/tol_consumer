import logging
from typing import Any

from lab_share_lib.processing.base_processor import BaseProcessor
from lab_share_lib.processing.rabbit_message import RabbitMessage
from lab_share_lib.rabbit.basic_publisher import BasicPublisher
from lab_share_lib.rabbit.schema_registry import SchemaRegistry

from tol_lab_share import error_codes
from tol_lab_share.messages.rabbit.consumed import BioscanPoolXpToTractionMessage
from tol_lab_share.messages.traction import TractionReceptionMessage

LOGGER = logging.getLogger(__name__)


class BioscanPoolXpToTractionProcessor(BaseProcessor):
    """Processor for consumed messages exporting Pool XP tubes to Traction."""

    def __init__(self, schema_registry: SchemaRegistry, config: Any):
        """Prepare the initial internal state of the processor.

        Args:
            schema_registry (SchemaRegistry): a schema registry for message parsing.
            config (Any): main configuration for the app.
        """
        LOGGER.debug("BioscanPoolXpToTractionProcessor::__init__")

        self._schema_registry = schema_registry
        self._config = config

    @staticmethod
    def instantiate(
        schema_registry: SchemaRegistry, _: BasicPublisher, config: Any
    ) -> "BioscanPoolXpToTractionProcessor":
        """Instantiate a BioscanPoolXpToTractionProcessor."""
        return BioscanPoolXpToTractionProcessor(schema_registry, config)

    def process(self, message: RabbitMessage) -> bool:
        """Processes a RabbitMQ message. The message will be parsed by BioscanPoolXpToTractionMessage and validated.
        If the message is correct, a new TractionReceptionMessage will be generated and sent to Traction.
        Note that no feedback message is generated for messages of this type, so message publishers will need to
        check the success of this process by polling the Traction API instead.

        Args:
            message (RabbitMessage) The RabbitMQ message to be processed.
        """
        LOGGER.debug("BioscanPoolXpToTractionProcessor::process")
        LOGGER.debug(f"Received: { message.message }")

        input = BioscanPoolXpToTractionMessage(message)

        if input.validate():
            traction_reception_message = TractionReceptionMessage()
            input.add_to_message_property(traction_reception_message)
            LOGGER.info("Attempting to send to traction")
            traction_reception_message.send(url=self._config.TRACTION_URL)

            if len(traction_reception_message.errors) > 0:
                error_codes.ERROR_16_PROBLEM_TALKING_WITH_TRACTION.trigger(
                    text=f":{traction_reception_message.errors}", instance=self
                )
                return False
        else:
            error_codes.ERROR_17_INPUT_MESSAGE_INVALID.trigger(text=f":{input.errors}", instance=self)
            return False

        return True
