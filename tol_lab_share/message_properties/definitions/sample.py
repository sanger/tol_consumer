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
from tol_lab_share.message_properties.definitions.genome_size import GenomeSize
from tol_lab_share.message_properties.definitions.accession_number import AccessionNumber
from tol_lab_share.message_properties.definitions.cost_code import CostCode


from tol_lab_share.constants.input_create_labware_message import (
    SAMPLE_PUBLIC_NAME,
    SAMPLE_COMMON_NAME,
    SAMPLE_CONCENTRATION,
    SAMPLE_COUNTRY_OF_ORIGIN,
    SAMPLE_DONOR_ID,
    SAMPLE_LIBRARY_TYPE,
    SAMPLE_LOCATION,
    SAMPLE_SANGER_SAMPLE_ID,
    SAMPLE_SANGER_TAXON_ID,
    SAMPLE_SANGER_UUID,
    SAMPLE_STUDY_UUID,
    SAMPLE_COLLECTION_DATE,
    SAMPLE_VOLUME,
    SAMPLE_ACCESSION_NUMBER,
    SAMPLE_GENOME_SIZE,
    SAMPLE_COST_CODE,
)
from typing import Any

import logging

logger = logging.getLogger(__name__)


class Sample(MessageProperty):
    """MessageProperty that handles the parsing of a labware section for the TOL message."""

    def __init__(self, input: Any):
        super().__init__(input)

        self.add_property("cost_code", CostCode(DictInput(input, SAMPLE_COST_CODE)))
        self.add_property("study_uuid", Uuid(DictInput(input, SAMPLE_STUDY_UUID)))
        self.add_property("common_name", CommonName(DictInput(input, SAMPLE_COMMON_NAME)))
        self.add_property("concentration", Concentration(DictInput(input, SAMPLE_CONCENTRATION)))
        self.add_property("volume", Volume(DictInput(input, SAMPLE_VOLUME)))
        self.add_property(
            "country_of_origin",
            CountryOfOrigin(DictInput(input, SAMPLE_COUNTRY_OF_ORIGIN)),
        )
        self.add_property("donor_id", DonorId(DictInput(input, SAMPLE_DONOR_ID)))
        self.add_property("library_type", LibraryType(DictInput(input, SAMPLE_LIBRARY_TYPE)))
        self.add_property("location", Location(DictInput(input, SAMPLE_LOCATION)))
        self.add_property("public_name", PublicName(DictInput(input, SAMPLE_PUBLIC_NAME)))
        self.add_property("sanger_sample_id", SangerSampleId(DictInput(input, SAMPLE_SANGER_SAMPLE_ID)))
        self.add_property(
            "scientific_name",
            ScientificNameFromTaxonId(TaxonId(DictInput(input, SAMPLE_SANGER_TAXON_ID))),
        )
        self.add_property("uuid", Uuid(DictInput(input, SAMPLE_SANGER_UUID)))
        self.add_property("accession_number", AccessionNumber(DictInput(input, SAMPLE_ACCESSION_NUMBER)))
        self.add_property("genome_size", GenomeSize(DictInput(input, SAMPLE_GENOME_SIZE)))
        self.add_property("collection_date", DateUtc(DictInput(input, SAMPLE_COLLECTION_DATE)))
