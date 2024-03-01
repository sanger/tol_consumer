from functools import singledispatchmethod
from lab_share_lib.processing.rabbit_message import RabbitMessage
from tol_lab_share.constants.input_create_labware_message import (
    MESSAGE_UUID,
    CREATED_DATE_UTC,
    LABWARE,
)
from tol_lab_share.messages.properties import MessageProperty
from tol_lab_share.messages.properties.complex import DateUtc, Labware, MessageUuid
from tol_lab_share.messages.properties.simple import DictValue

import logging

from tol_lab_share.messages.rabbit.published import CreateLabwareFeedbackMessage

logger = logging.getLogger(__name__)


class CreateLabwareMessage(MessageProperty):
    """Class that handles parsing a TOL lab share message received"""

    def __init__(self, m: RabbitMessage):
        """Constructor that receives a RabbitMessage and parses it using the properties defined.

        Args:
            m (RabbitMessage): The message to parse.
        """
        super().__init__(m)
        self._message = m.message

        self.add_property("message_uuid", MessageUuid(DictValue(self._message, MESSAGE_UUID)))
        self.add_property("labware", Labware(DictValue(self._message, LABWARE)))
        self.add_property("create_date_utc", DateUtc(DictValue(self._message, CREATED_DATE_UTC)))

    @singledispatchmethod
    def add_to_message_property(self, message_property: MessageProperty) -> None:
        super().add_to_message_property(message_property)

    @add_to_message_property.register
    def _(self, feedback_message: CreateLabwareFeedbackMessage) -> None:
        """Adds errors from this message into an CreateLabwareFeedbackMessage.
        If errors are added, it will change the operation_was_error_free flag to False.

        Args:
            feedback_message (CreateLabwareFeedbackMessage): The CreateLabwareFeedbackMessage to add errors to.
        """
        logger.debug("ValueCreateLabware::add_to_message_property")
        super().add_to_message_property(feedback_message)

        if len(self.errors) > 0:
            for error in self.errors:
                feedback_message.add_error(error)
            feedback_message.operation_was_error_free = False
