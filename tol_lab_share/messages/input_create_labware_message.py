from lab_share_lib.processing.rabbit_message import RabbitMessage
from .output_feedback_message import OutputFeedbackMessage

from tol_lab_share.constants import (
    INPUT_CREATE_LABWARE_MESSAGE_MESSAGE_UUID, 
    INPUT_CREATE_LABWARE_MESSAGE_CREATED_DATE_UTC, INPUT_CREATE_LABWARE_MESSAGE_LABWARE
)

from tol_lab_share.message_properties import Uuid, Labware, CreatedDateUtc

class InputCreateLabwareMessage:
    def __init__(self, m: RabbitMessage):
        self._message = m.message

        self._uuid = Uuid(self._message[INPUT_CREATE_LABWARE_MESSAGE_MESSAGE_UUID])
        self._createDateUtc = CreatedDateUtc(self._message[INPUT_CREATE_LABWARE_MESSAGE_CREATED_DATE_UTC])
        self._labware = Labware(self._message[INPUT_CREATE_LABWARE_MESSAGE_LABWARE])
        self._components = [self._uuid, self._createDateUtc, self._labware]

    def validate(self):
        return all([comp.validate() for comp in self._components])

    def add_to_feedback_message(self, feedback_message: OutputFeedbackMessage):
        return True