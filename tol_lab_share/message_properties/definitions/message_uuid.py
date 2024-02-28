from functools import singledispatchmethod
from tol_lab_share.messages.properties.message_property import MessageProperty
from tol_lab_share.message_properties.definitions.uuid import Uuid

import logging

from tol_lab_share.messages.output_feedback_message import OutputFeedbackMessage

logger = logging.getLogger(__name__)


class MessageUuid(Uuid):
    """Uuid subclass to manage parsing of a valid message uuid string provided by the superclass
    Uuid.
    """

    @singledispatchmethod
    def add_to_message_property(self, message_property: MessageProperty) -> None:
        super().add_to_message_property(message_property)

    @add_to_message_property.register
    def _(self, feedback_message: OutputFeedbackMessage) -> None:
        """Adds the source message uuid to the feedback message passed as parameter

        Parameters:
            feedback_message (OutputFeedbacMessage) message where we want to add the info
        """
        logger.debug("MessageUuid::add_to_message_property")
        super().add_to_message_property(feedback_message)
        feedback_message.source_message_uuid = self.value
