from typing import Any

from .labware_type import LabwareType
from tol_lab_share.messages.properties.message_specific import CreateLabwareSample
from tol_lab_share.constants import OUTPUT_TRACTION_MESSAGE_CONTAINER_TYPES
from tol_lab_share.constants.input_create_labware_message import BARCODE, LABWARE_TYPE, SAMPLES, RETENTION_INSTRUCTION
from tol_lab_share.messages.properties.simple import DictValue, StringValue
from tol_lab_share.messages.rabbit.published import CreateLabwareFeedbackMessage
from tol_lab_share.messages.traction import TractionReceptionMessage, TractionQcMessage

from tol_lab_share.messages.properties import MessageProperty
from functools import singledispatchmethod

import logging

logger = logging.getLogger(__name__)


class Labware(MessageProperty):
    """MessageProperty that handles the parsing of a labware section for the TOL message."""

    def __init__(self, input: MessageProperty):
        super().__init__(input)

        self.add_property("labware_type", LabwareType(DictValue(input, LABWARE_TYPE)))
        self.add_property("barcode", StringValue(DictValue(input, BARCODE)))
        self.add_property("samples", self._parse_samples(input))
        self.add_property("retention_instruction", StringValue(DictValue(input, RETENTION_INSTRUCTION)))

    def _parse_samples(self, input: MessageProperty) -> list[MessageProperty]:
        """Parses the samples section and creates a sample for each position."""
        samples_dict = DictValue(input, SAMPLES)
        if samples_dict.validate():
            samples_list_dict: list[MessageProperty] = []
            for position in range(len(samples_dict.value)):
                sample = samples_dict.value[position]
                samples_list_dict.append(CreateLabwareSample(sample))
        else:
            samples_list_dict = [samples_dict]
        return samples_list_dict

    def labware_type(self) -> Any:
        """Returns the instance of LabwareType to is a property to this instance."""
        return self.properties("labware_type")

    def count_of_total_samples(self) -> int:
        """Returns the number of total samples inside this labware"""
        return len(self._properties["samples"])

    def count_of_valid_samples(self) -> int:
        """Returns the number of samples that are valid from this labware"""
        return [sample.validate() for sample in self._properties["samples"]].count(True)

    def traction_container_type(self) -> OUTPUT_TRACTION_MESSAGE_CONTAINER_TYPES:
        """It converts the labware type to a valid container type value for Traction.

        Returns:
            str with a container type value for Traction
        """
        if self.labware_type().value == "Tube":
            return "tubes"
        else:
            return "wells"

    @singledispatchmethod
    def add_to_message_property(self, message_property: MessageProperty) -> None:
        super().add_to_message_property(message_property)

    @add_to_message_property.register
    def _(self, feedback_message: CreateLabwareFeedbackMessage) -> None:
        """Adds the labware information to an CreateLabwareFeedbackMessage.
        This includes the number of total samples and the number of valid samples.

        Args:
            feedback_message (CreateLabwareFeedbackMessage): The feedback message to add the data to.
        """
        logger.debug("Labware::add_to_message_property")
        super().add_to_message_property(feedback_message)

        feedback_message.count_of_total_samples = self.count_of_total_samples()
        feedback_message.count_of_valid_samples = self.count_of_valid_samples()

    @add_to_message_property.register
    def _(self, message: TractionReceptionMessage) -> None:
        """Adds the labware information to a TractionReceptionMessage.

        Args:
            message (TractionReceptionMessage): The Traction reception message to add the data to.
        """
        super().add_to_message_property(message)

        for sample in self.properties("samples"):
            request = message.create_request()
            request.accession_number = sample.properties("accession_number").value
            request.container_barcode = self.properties("barcode").value
            request.container_location = sample.properties("location").value
            request.container_type = self.traction_container_type()
            request.cost_code = sample.properties("cost_code").value
            request.country_of_origin = sample.properties("country_of_origin").value
            request.date_of_sample_collection = sample.properties("collection_date").value
            request.donor_id = sample.properties("donor_id").value
            request.genome_size = sample.properties("genome_size").value
            request.library_type = sample.properties("library_type").value
            request.priority_level = sample.properties("priority_level").value
            request.public_name = sample.properties("public_name").value
            request.sample_name = sample.properties("sanger_sample_id").value
            request.sample_uuid = sample.properties("uuid").value
            request.sanger_sample_id = sample.properties("sanger_sample_id").value
            request.species = sample.properties("scientific_name").value
            request.study_uuid = sample.properties("study_uuid").value
            request.supplier_name = sample.properties("supplier_sample_name").value
            request.taxon_id = sample.properties("taxon_id").value

    @add_to_message_property.register
    def _(self, message: TractionQcMessage) -> None:
        """Adds the QC data for this labware to a TractionQcMessage.

        Args:
            message (TractionQcMessage): The Traction QC message to add the data to.
        """
        super().add_to_message_property(message)

        for sample in self.properties("samples"):
            request = message.create_request()
            request.sheared_femto_fragment_size = sample.properties("sheared_femto_fragment_size").value
            request.post_spri_concentration = sample.properties("post_spri_concentration").value
            request.post_spri_volume = sample.properties("post_spri_volume").value
            request.final_nano_drop_280 = sample.properties("final_nano_drop_280").value
            request.final_nano_drop_230 = sample.properties("final_nano_drop_230").value
            request.final_nano_drop = sample.properties("final_nano_drop").value
            request.shearing_qc_comments = sample.properties("shearing_qc_comments").value
            request.date_submitted_utc = sample.properties("date_submitted_utc").value
            request.container_barcode = self.properties("barcode").value
            request.sanger_sample_id = sample.properties("sanger_sample_id").value
