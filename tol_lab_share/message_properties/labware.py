from .message_property import MessageProperty
from tol_lab_share.message_properties.labware_type import LabwareType
from tol_lab_share.message_properties.barcode import Barcode
from tol_lab_share.message_properties.uuid import Uuid
from tol_lab_share.message_properties.sample import Sample
from tol_lab_share.messages.output_feedback_message import OutputFeedbackMessage
from tol_lab_share.message_properties.dict_input import DictInput
from typing import List

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
            samples_list_dict: List[MessageProperty] = []
            for position in range(len(samples_dict.value)):
                sample = samples_dict.value[position]
                samples_list_dict.append(Sample(sample, self, position))
        else:
            samples_list_dict = [samples_dict]

        self._properties = {
            "labware_uuid": Uuid(DictInput(input, INPUT_CREATE_LABWARE_MESSAGE_UUID)),
            "labware_type": labware_type,
            "barcode": Barcode(DictInput(input, INPUT_CREATE_LABWARE_MESSAGE_BARCODE)),
            "samples": samples_list_dict,
        }

    def labware_type(self):
        return self._properties["labware_type"]

    def container_type(self):
        if self._properties["labware_type"].value == "Tube":
            return "tubes"
        else:
            return "wells"

    def count_of_total_samples(self):
        return len(self._properties["samples"])

    def count_of_valid_samples(self):
        return [sample.validate() for sample in self._properties["samples"]].count(True)

    def add_to_feedback_message(self, feedback_message: OutputFeedbackMessage) -> None:
        logger.debug("Labware::add_to_feedback_message")
        super().add_to_feedback_message(feedback_message)
        feedback_message.count_of_total_samples = self.count_of_total_samples()
        feedback_message.count_of_valid_samples = self.count_of_valid_samples()
