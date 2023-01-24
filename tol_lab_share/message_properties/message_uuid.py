from tol_lab_share.message_properties.uuid import Uuid
from tol_lab_share.messages.output_feedback_message import OutputFeedbackMessage

import logging

logger = logging.getLogger(__name__)


class MessageUuid(Uuid):
    def add_to_feedback_message(self, feedback_message: OutputFeedbackMessage) -> None:
        logger.debug("MessageUuid::add_to_feedback_message")
        super().add_to_feedback_message(feedback_message)
        feedback_message.source_message_uuid = self.value
