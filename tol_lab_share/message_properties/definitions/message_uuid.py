from tol_lab_share.message_properties.definitions.uuid import Uuid
from tol_lab_share.messages.interfaces import OutputFeedbackMessageInterface

import logging

logger = logging.getLogger(__name__)


class MessageUuid(Uuid):
    """Uuid subclass to manage parsing of a valid message uuid string provided by the superclass
    Uuid.
    """

    def add_to_feedback_message(self, feedback_message: OutputFeedbackMessageInterface) -> None:
        """Adds the source message uuid to the feedback message passed as parameter
        Parameters:
        feedback_message (OutputFeedbacMessageInterface) message where we want to add the info
        """
        logger.debug("MessageUuid::add_to_feedback_message")
        super().add_to_feedback_message(feedback_message)
        feedback_message.source_message_uuid = self.value
