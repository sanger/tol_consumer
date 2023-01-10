from .message_property import MessageProperty
from tol_lab_share.message_properties.labware_type import LabwareType
from tol_lab_share.message_properties.barcode import Barcode
from tol_lab_share.message_properties.uuid import Uuid
from tol_lab_share.message_properties.sample import Sample
from tol_lab_share.data_resolvers.data_resolver import DataResolver
from tol_lab_share.messages.output_feedback_message import OutputFeedbackMessage
from tol_lab_share.message_properties.dict_input import DictInput

from tol_lab_share.constants import (
    INPUT_CREATE_LABWARE_MESSAGE_LABWARE_TYPE,
    INPUT_CREATE_LABWARE_MESSAGE_BARCODE,
    INPUT_CREATE_LABWARE_MESSAGE_SAMPLES,
    INPUT_CREATE_LABWARE_MESSAGE_UUID,
)
import logging

logger = logging.getLogger(__name__)


class Labware(MessageProperty):
    def __init__(self, input):
        super().__init__(input)
        labware_type = LabwareType(DictInput(input, INPUT_CREATE_LABWARE_MESSAGE_LABWARE_TYPE))
        samples_dict = DictInput(input, INPUT_CREATE_LABWARE_MESSAGE_SAMPLES)
        if samples_dict.validate():
            samples_list_dict = list([DataResolver(Sample(labware_type, sample)) for sample in samples_dict.value])
        else:
            samples_list_dict = [DataResolver(samples_dict)]

        self._properties = {
            "labware_uuid": DataResolver(Uuid(DictInput(input, INPUT_CREATE_LABWARE_MESSAGE_UUID))),
            "labware_type": DataResolver(labware_type),
            "barcode": DataResolver(Barcode(DictInput(input, INPUT_CREATE_LABWARE_MESSAGE_BARCODE))),
            "samples": samples_list_dict,
        }

    def add_to_feedback_message(self, feedback_message: OutputFeedbackMessage) -> None:
        logger.debug("Labware::add_to_feedback_message")
        super().add_to_feedback_message(feedback_message)
        feedback_message.count_of_total_samples = 96
        feedback_message.count_of_valid_samples = 96
