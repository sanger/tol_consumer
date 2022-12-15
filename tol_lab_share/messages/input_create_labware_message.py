from lab_share_lib.processing.rabbit_message import RabbitMessage
from .output_feedback_message import OutputFeedbackMessage

from tol_lab_share.constants import (
    INPUT_CREATE_LABWARE_MESSAGE_MESSAGE_UUID,
    INPUT_CREATE_LABWARE_MESSAGE_CREATED_DATE_UTC,
    INPUT_CREATE_LABWARE_MESSAGE_LABWARE,
)

from tol_lab_share.message_properties import Uuid, Labware, CreatedDateUtc


class InputCreateLabwareMessage:
    def __init__(self, m: RabbitMessage):
        self._message = m.message

        self._properties = {
            'uuid': Uuid(self._message[INPUT_CREATE_LABWARE_MESSAGE_MESSAGE_UUID]),
            'labware': Labware(self._message[INPUT_CREATE_LABWARE_MESSAGE_LABWARE]),
            'create_date_utc': CreatedDateUtc(self._message[INPUT_CREATE_LABWARE_MESSAGE_CREATED_DATE_UTC]) 
        }

    def validate(self) -> bool:
        return all([self._properties[prop_name].validate() for prop_name in self._properties.keys()])

    def resolve(self) -> bool:
        for prop_name in self._properties.keys():
            self._properties[prop_name].resolve()

    def add_to_feedback_message(self, feedback_message: OutputFeedbackMessage) -> bool:
        for prop_name in self._properties.keys():
            self._properties[prop_name].add_to_feedback_message(feedback_message)
        return True
