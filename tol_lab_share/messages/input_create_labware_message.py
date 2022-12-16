from lab_share_lib.processing.rabbit_message import RabbitMessage
from .output_feedback_message import OutputFeedbackMessage
from typing import List
from tol_lab_share.constants import (
    INPUT_CREATE_LABWARE_MESSAGE_MESSAGE_UUID,
    INPUT_CREATE_LABWARE_MESSAGE_CREATED_DATE_UTC,
    INPUT_CREATE_LABWARE_MESSAGE_LABWARE,
)
import itertools
from tol_lab_share.message_properties.uuid import Uuid
from tol_lab_share.message_properties.labware import Labware
from tol_lab_share.message_properties.created_date_utc import CreatedDateUtc
from tol_lab_share.state_machines.data_resolution import DataResolution
from tol_lab_share.error_codes import ErrorCode


class InputCreateLabwareMessage:
    def __init__(self, m: RabbitMessage):
        self._message = m.message

        self._properties = {
            "uuid": Uuid(self._message[INPUT_CREATE_LABWARE_MESSAGE_MESSAGE_UUID]),
            "labware": Labware(self._message[INPUT_CREATE_LABWARE_MESSAGE_LABWARE]),
            "create_date_utc": CreatedDateUtc(self._message[INPUT_CREATE_LABWARE_MESSAGE_CREATED_DATE_UTC]),
        }
        self.state = DataResolution()

    def validate(self) -> bool:
        self.state.performing_validation()

        result = all([self._properties[prop_name].validate() for prop_name in self._properties.keys()])
        if result:
            self.state.validation_passed()
        else:
            self.state.validation_failed()

        return result

    @property
    def errors(self) -> List[ErrorCode]:
        list_of_lists = [self._properties[prop_name].errors for prop_name in self._properties.keys()]
        return list(itertools.chain(*list_of_lists))

    def resolve(self) -> bool:
        self.state.request_resolution()

        for prop_name in self._properties.keys():
            self._properties[prop_name].resolve()

        self.state.resolution_successful()
        return True

    def add_to_feedback_message(self, feedback_message: OutputFeedbackMessage) -> bool:
        self.state.retrieve_feedback()

        for prop_name in self._properties.keys():
            self._properties[prop_name].add_to_feedback_message(feedback_message)
        return True
