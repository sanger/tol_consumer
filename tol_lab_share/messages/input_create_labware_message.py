from lab_share_lib.processing.rabbit_message import RabbitMessage
from tol_lab_share.constants import (
    INPUT_CREATE_LABWARE_MESSAGE_MESSAGE_UUID,
    INPUT_CREATE_LABWARE_MESSAGE_CREATED_DATE_UTC,
    INPUT_CREATE_LABWARE_MESSAGE_LABWARE,
)
from tol_lab_share.message_properties.message_uuid import MessageUuid
from tol_lab_share.message_properties.labware import Labware
from tol_lab_share.message_properties.date_utc import DateUtc
from tol_lab_share.message_properties.message_property import MessageProperty
from tol_lab_share.message_properties.dict_input import DictInput


class InputCreateLabwareMessage(MessageProperty):
    def __init__(self, m: RabbitMessage):
        super().__init__(m)
        self._message = m.message
        self._properties = {
            "uuid": MessageUuid(DictInput(self._message, INPUT_CREATE_LABWARE_MESSAGE_MESSAGE_UUID)),
            "labware": Labware(DictInput(self._message, INPUT_CREATE_LABWARE_MESSAGE_LABWARE)),
            "create_date_utc": DateUtc(DictInput(self._message, INPUT_CREATE_LABWARE_MESSAGE_CREATED_DATE_UTC)),
        }
