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
from tol_lab_share.error_codes import ErrorCode
from tol_lab_share.data_resolvers.data_resolver import DataResolver
from tol_lab_share.data_resolvers.data_resolver_interface import DataResolverInterface
from functools import cached_property
from typing import Any


class InputCreateLabwareMessage(DataResolverInterface):
    def __init__(self, m: RabbitMessage):
        self._message = m.message

        self._properties = {
            "uuid": DataResolver(Uuid(self._message[INPUT_CREATE_LABWARE_MESSAGE_MESSAGE_UUID])),
            "labware": DataResolver(Labware(self._message[INPUT_CREATE_LABWARE_MESSAGE_LABWARE])),
            "create_date_utc": DataResolver(
                CreatedDateUtc(self._message[INPUT_CREATE_LABWARE_MESSAGE_CREATED_DATE_UTC])
            ),
        }

    def validate(self) -> bool:
        result_list = [self._properties[prop_name].validate() for prop_name in self._properties.keys()]
        return all(result_list)

    @property
    def errors(self) -> List[ErrorCode]:
        list_of_lists = [self._properties[prop_name].errors for prop_name in self._properties.keys()]
        return list(itertools.chain(*list_of_lists))

    def resolve(self) -> bool:
        for prop_name in self._properties.keys():
            if self._properties[prop_name].state.is_valid:
                self._properties[prop_name].resolve()
        return True

    def add_to_feedback_message(self, feedback_message: OutputFeedbackMessage) -> None:
        self.validate()
        self.resolve()
        for prop_name in self._properties.keys():
            self._properties[prop_name].add_to_feedback_message(feedback_message)

    @cached_property
    def value(self) -> Any:
        return True
