from functools import singledispatchmethod
from tol_lab_share.messages.properties import MessageProperty
from .uuid import Uuid

import logging

from tol_lab_share.messages.rabbit.published import CreateLabwareFeedbackMessage

logger = logging.getLogger(__name__)


class MessageUuid(Uuid):
    """Uuid subclass to manage parsing of a valid message uuid string provided by the superclass
    Uuid.
    """

    @singledispatchmethod
    def add_to_message_property(self, message_property: MessageProperty) -> None:
        super().add_to_message_property(message_property)

    @add_to_message_property.register
    def _(self, feedback_message: CreateLabwareFeedbackMessage) -> None:
        """Adds the source message uuid to the feedback message passed as parameter

        Parameters:
            feedback_message (OutputFeedbacMessage) message where we want to add the info
        """
        logger.debug("MessageUuid::add_to_message_property")
        super().add_to_message_property(feedback_message)
        feedback_message.source_message_uuid = self.value
