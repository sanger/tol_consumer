import logging
from typing import Any

from lab_share_lib.processing.base_processor import BaseProcessor
from lab_share_lib.processing.rabbit_message import RabbitMessage
from lab_share_lib.rabbit.basic_publisher import BasicPublisher
from lab_share_lib.rabbit.schema_registry import SchemaRegistry

from tol_lab_share import error_codes
from tol_lab_share.messages.consumed import BioscanPoolXpToTractionMessage, BioscanPoolXpToTractionValidator
from tol_lab_share.messages.mappers.bioscan_pool_xp_to_traction import BioscanPoolXpToTractionMapper
from tol_lab_share.messages.traction import TractionReceptionMessage

LOGGER = logging.getLogger(__name__)


class BioscanPoolXpToTractionProcessor(BaseProcessor):
    """Processor for consumed messages exporting Pool XP tubes to Traction."""

    def __init__(self, config: Any):
        """Prepare the initial internal state of the processor.

        Args:
            config (Any): main configuration for the app.
        """
        LOGGER.debug("BioscanPoolXpToTractionProcessor::__init__")

        self._config = config

    @staticmethod
    def instantiate(
        _schema_registry: SchemaRegistry, _basic_publisher: BasicPublisher, config: Any
    ) -> "BioscanPoolXpToTractionProcessor":
        """Instantiate a BioscanPoolXpToTractionProcessor."""
        return BioscanPoolXpToTractionProcessor(config)

    def process(self, rabbit_message: RabbitMessage) -> bool:
        """Processes a RabbitMQ message. The message will be parsed by BioscanPoolXpToTractionMessage and validated.
        If the message is correct, a new TractionReceptionMessage will be generated and sent to Traction.
        Note that no feedback message is generated for messages of this type, so message publishers will need to
        check the success of this process by polling the Traction API instead.

        Args:
            rabbit_message (RabbitMessage) The RabbitMQ message to be processed.
        """
        LOGGER.debug("BioscanPoolXpToTractionProcessor::process")

        message = BioscanPoolXpToTractionMessage(rabbit_message.message)
        validator = BioscanPoolXpToTractionValidator(message)

        if validator.validate():
            traction_reception_message = TractionReceptionMessage()
            BioscanPoolXpToTractionMapper.map(message, traction_reception_message)

            LOGGER.info("Attempting to send to traction")
            traction_reception_message.send(url=self._config.TRACTION_URL)

            if len(traction_reception_message.errors) > 0:
                error_codes.ERROR_16_PROBLEM_TALKING_WITH_TRACTION.trigger(
                    text=f":{traction_reception_message.errors}", instance=self
                )
                return False
        else:
            error_codes.ERROR_17_INPUT_MESSAGE_INVALID.trigger(text=f":{validator.errors}", instance=self)
            return False

        return True
