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
from tol_lab_share.data_resolvers.data_resolver import DataResolver
from tol_lab_share.message_properties.dict_input import DictInput


class InputCreateLabwareMessage(MessageProperty):
    def __init__(self, m: RabbitMessage):
        super().__init__(m)
        self._message = m.message
        self._properties = {
            "uuid": DataResolver(MessageUuid(DictInput(self._message, INPUT_CREATE_LABWARE_MESSAGE_MESSAGE_UUID))),
            "labware": DataResolver(Labware(DictInput(self._message, INPUT_CREATE_LABWARE_MESSAGE_LABWARE))),
            "create_date_utc": DataResolver(
                DateUtc(DictInput(self._message, INPUT_CREATE_LABWARE_MESSAGE_CREATED_DATE_UTC))
            ),
        }

    # def validate(self) -> bool:
    #     result_list = [self._properties[prop_name].validate() for prop_name in self._properties.keys()]
    #     return all(result_list)

    # @property
    # def errors(self) -> List[ErrorCode]:
    #     list_of_lists = [self._properties[prop_name].errors for prop_name in self._properties.keys()]
    #     return list(itertools.chain(*list_of_lists))

    # def resolve(self) -> bool:
    #     for prop_name in self._properties.keys():
    #         if self._properties[prop_name].state.is_valid:
    #             self._properties[prop_name].resolve()
    #     return True

    # def add_to_feedback_message(self, feedback_message: OutputFeedbackMessage) -> None:
    #     self.validate()
    #     self.resolve()
    #     for prop_name in self._properties.keys():
    #         self._properties[prop_name].add_to_feedback_message(feedback_message)

    # def add_to_traction_message(self, traction_message: OutputTractionMessage):

    # @cached_property
    # def value(self) -> Any:
    #     return True
