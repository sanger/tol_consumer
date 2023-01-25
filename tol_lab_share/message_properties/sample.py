from .message_property import MessageProperty
from tol_lab_share.message_properties.public_name import PublicName
from tol_lab_share.message_properties.common_name import CommonName
from tol_lab_share.message_properties.concentration import Concentration
from tol_lab_share.message_properties.volume import Volume
from tol_lab_share.message_properties.country_of_origin import CountryOfOrigin
from tol_lab_share.message_properties.donor_id import DonorId
from tol_lab_share.message_properties.library_type import LibraryType
from tol_lab_share.message_properties.location import Location, PaddedLocationString
from tol_lab_share.message_properties.sanger_sample_id import SangerSampleId
from tol_lab_share.message_properties.taxon_id import TaxonId
from tol_lab_share.message_properties.scientific_name_from_taxon_id import ScientificNameFromTaxonId
from tol_lab_share.message_properties.uuid import Uuid
from tol_lab_share.message_properties.dict_input import DictInput
from tol_lab_share.message_properties.date_utc import DateUtc

from tol_lab_share.messages.output_traction_message import OutputTractionMessage

from tol_lab_share.constants import (
    INPUT_CREATE_LABWARE_MESSAGE_SAMPLE_PUBLIC_NAME,
    INPUT_CREATE_LABWARE_MESSAGE_SAMPLE_COMMON_NAME,
    INPUT_CREATE_LABWARE_MESSAGE_SAMPLE_CONCENTRATION,
    INPUT_CREATE_LABWARE_MESSAGE_SAMPLE_COUNTRY_OF_ORIGIN,
    INPUT_CREATE_LABWARE_MESSAGE_SAMPLE_DONOR_ID,
    INPUT_CREATE_LABWARE_MESSAGE_SAMPLE_LIBRARY_TYPE,
    INPUT_CREATE_LABWARE_MESSAGE_SAMPLE_LOCATION,
    INPUT_CREATE_LABWARE_MESSAGE_SAMPLE_SANGER_SAMPLE_ID,
    INPUT_CREATE_LABWARE_MESSAGE_SAMPLE_SANGER_TAXON_ID,
    INPUT_CREATE_LABWARE_MESSAGE_SAMPLE_SANGER_UUID,
    INPUT_CREATE_LABWARE_MESSAGE_SAMPLE_STUDY_UUID,
    INPUT_CREATE_LABWARE_MESSAGE_SAMPLE_COLLECTION_DATE,
    INPUT_CREATE_LABWARE_MESSAGE_SAMPLE_VOLUME,
)

import logging

logger = logging.getLogger(__name__)


class Sample(MessageProperty):
    def __init__(self, input):
        super().__init__(input)

        self.add_property("study_uuid", Uuid(DictInput(input, INPUT_CREATE_LABWARE_MESSAGE_SAMPLE_STUDY_UUID)))
        self.add_property("common_name", CommonName(DictInput(input, INPUT_CREATE_LABWARE_MESSAGE_SAMPLE_COMMON_NAME)))
        self.add_property(
            "concentration", Concentration(DictInput(input, INPUT_CREATE_LABWARE_MESSAGE_SAMPLE_CONCENTRATION))
        )
        self.add_property("volume", Volume(DictInput(input, INPUT_CREATE_LABWARE_MESSAGE_SAMPLE_VOLUME)))
        self.add_property(
            "country_of_origin",
            CountryOfOrigin(DictInput(input, INPUT_CREATE_LABWARE_MESSAGE_SAMPLE_COUNTRY_OF_ORIGIN)),
        )
        self.add_property("donor_id", DonorId(DictInput(input, INPUT_CREATE_LABWARE_MESSAGE_SAMPLE_DONOR_ID)))
        self.add_property(
            "library_type", LibraryType(DictInput(input, INPUT_CREATE_LABWARE_MESSAGE_SAMPLE_LIBRARY_TYPE))
        )
        self.add_property(
            "location", Location(PaddedLocationString(DictInput(input, INPUT_CREATE_LABWARE_MESSAGE_SAMPLE_LOCATION)))
        )
        self.add_property("public_name", PublicName(DictInput(input, INPUT_CREATE_LABWARE_MESSAGE_SAMPLE_PUBLIC_NAME)))
        self.add_property(
            "sanger_sample_id", SangerSampleId(DictInput(input, INPUT_CREATE_LABWARE_MESSAGE_SAMPLE_SANGER_SAMPLE_ID))
        )
        self.add_property(
            "scientific_name",
            ScientificNameFromTaxonId(TaxonId(DictInput(input, INPUT_CREATE_LABWARE_MESSAGE_SAMPLE_SANGER_TAXON_ID))),
        )
        self.add_property("uuid", Uuid(DictInput(input, INPUT_CREATE_LABWARE_MESSAGE_SAMPLE_SANGER_UUID)))
        self.add_property(
            "collection_date", DateUtc(DictInput(input, INPUT_CREATE_LABWARE_MESSAGE_SAMPLE_COLLECTION_DATE))
        )

    def position(self):
        if self.property_position is None:
            return "Empty"
        return self.property_position

    def labware(self):
        return self.property_source

    def unpadded_location(self):
        text = self.properties("location").value
        if text and len(text) == 3 and text[1] == "0":
            return f"{text[0]}{text[2]}"
        return text

    def add_to_traction_message(self, traction_message: OutputTractionMessage) -> None:
        super().add_to_traction_message(traction_message)
        traction_message.requests(self.position()).study_uuid = self.properties("study_uuid").value
        traction_message.requests(self.position()).sample_name = self.properties("public_name").value
        traction_message.requests(self.position()).sample_uuid = self.properties("uuid").value
        traction_message.requests(self.position()).library_type = self.properties("library_type").value
        traction_message.requests(self.position()).species = self.properties("scientific_name").value
        traction_message.requests(self.position()).container_barcode = self.labware().properties("barcode").value
        traction_message.requests(self.position()).container_location = self.unpadded_location()
        traction_message.requests(self.position()).container_type = self.labware().traction_container_type()
