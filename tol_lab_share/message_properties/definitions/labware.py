from .message_property import MessageProperty
from tol_lab_share.message_properties.definitions.labware_type import LabwareType
from tol_lab_share.message_properties.definitions.barcode import Barcode

from tol_lab_share.message_properties.definitions.sample import Sample
from tol_lab_share.messages.interfaces import OutputFeedbackMessageInterface
from tol_lab_share.message_properties.definitions.dict_input import DictInput
from typing import List
from tol_lab_share.constants import (
    OUTPUT_TRACTION_MESSAGE_CREATE_REQUEST_CONTAINER_TYPE_TUBES,
    OUTPUT_TRACTION_MESSAGE_CREATE_REQUEST_CONTAINER_TYPE_WELLS,
)

from tol_lab_share.constants import (
    INPUT_CREATE_LABWARE_MESSAGE_LABWARE_TYPE,
    INPUT_CREATE_LABWARE_MESSAGE_BARCODE,
    INPUT_CREATE_LABWARE_MESSAGE_SAMPLES,
)
from tol_lab_share.messages.output_traction_message import OutputTractionMessageInterface

import logging

logger = logging.getLogger(__name__)


class Labware(MessageProperty):
    def __init__(self, input):
        super().__init__(input)

        self.add_property("labware_type", LabwareType(DictInput(input, INPUT_CREATE_LABWARE_MESSAGE_LABWARE_TYPE)))
        self.add_property("barcode", Barcode(DictInput(input, INPUT_CREATE_LABWARE_MESSAGE_BARCODE)))
        self.add_property("samples", self._parse_samples(input))

    def _parse_samples(self, input):
        samples_dict = DictInput(input, INPUT_CREATE_LABWARE_MESSAGE_SAMPLES)
        if samples_dict.validate():
            samples_list_dict: List[MessageProperty] = []
            for position in range(len(samples_dict.value)):
                sample = samples_dict.value[position]
                samples_list_dict.append(Sample(sample))
        else:
            samples_list_dict = [samples_dict]
        return samples_list_dict

    def labware_type(self):
        return self.properties("labware_type")

    def count_of_total_samples(self):
        return len(self._properties["samples"])

    def count_of_valid_samples(self):
        return [sample.validate() for sample in self._properties["samples"]].count(True)

    def add_to_feedback_message(self, feedback_message: OutputFeedbackMessageInterface) -> None:
        logger.debug("Labware::add_to_feedback_message")
        super().add_to_feedback_message(feedback_message)
        feedback_message.count_of_total_samples = self.count_of_total_samples()
        feedback_message.count_of_valid_samples = self.count_of_valid_samples()

    def traction_container_type(self):
        if self.labware_type().value == "Tube":
            return OUTPUT_TRACTION_MESSAGE_CREATE_REQUEST_CONTAINER_TYPE_TUBES
        else:
            return OUTPUT_TRACTION_MESSAGE_CREATE_REQUEST_CONTAINER_TYPE_WELLS

    def add_to_traction_message(self, traction_message: OutputTractionMessageInterface) -> None:
        super().add_to_traction_message(traction_message)
        for sample_pos in range(len(self.properties("samples"))):
            sample = self.properties("samples")[sample_pos]
            traction_message.requests(sample_pos).study_uuid = sample.properties("study_uuid").value
            traction_message.requests(sample_pos).sample_name = sample.properties("public_name").value
            traction_message.requests(sample_pos).sample_uuid = sample.properties("uuid").value
            traction_message.requests(sample_pos).library_type = sample.properties("library_type").value
            traction_message.requests(sample_pos).species = sample.properties("scientific_name").value
            traction_message.requests(sample_pos).container_barcode = self.properties("barcode").value
            traction_message.requests(sample_pos).container_location = sample.properties("location").value
            traction_message.requests(sample_pos).container_type = self.traction_container_type()
