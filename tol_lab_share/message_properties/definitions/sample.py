from .message_property import MessageProperty
from tol_lab_share.message_properties.definitions.public_name import PublicName
from tol_lab_share.message_properties.definitions.common_name import CommonName
from tol_lab_share.message_properties.definitions.concentration import Concentration
from tol_lab_share.message_properties.definitions.volume import Volume
from tol_lab_share.message_properties.definitions.country_of_origin import CountryOfOrigin
from tol_lab_share.message_properties.definitions.donor_id import DonorId
from tol_lab_share.message_properties.definitions.library_type import LibraryType
from tol_lab_share.message_properties.definitions.location import Location
from tol_lab_share.message_properties.definitions.sanger_sample_id import SangerSampleId
from tol_lab_share.message_properties.definitions.taxon_id import TaxonId
from tol_lab_share.message_properties.definitions.scientific_name_from_taxon_id import ScientificNameFromTaxonId
from tol_lab_share.message_properties.definitions.uuid import Uuid
from tol_lab_share.message_properties.definitions.dict_input import DictInput
from tol_lab_share.message_properties.definitions.date_utc import DateUtc


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
        self.add_property("location", Location(DictInput(input, INPUT_CREATE_LABWARE_MESSAGE_SAMPLE_LOCATION)))
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
