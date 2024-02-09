import logging
from typing import Any

from tol_lab_share.constants.input_create_labware_message import (
    DATE_SUBMITTED_UTC,
    FINAL_NANODROP,
    FINAL_NANODROP_230,
    FINAL_NANODROP_280,
    POST_SPRI_CONCENTRATION,
    POST_SPRI_VOLUME,
    PRIORITY_LEVEL,
    SAMPLE_ACCESSION_NUMBER,
    SAMPLE_COLLECTION_DATE,
    SAMPLE_COMMON_NAME,
    SAMPLE_CONCENTRATION,
    SAMPLE_COST_CODE,
    SAMPLE_COUNTRY_OF_ORIGIN,
    SAMPLE_DONOR_ID,
    SAMPLE_GENOME_SIZE,
    SAMPLE_LIBRARY_TYPE,
    SAMPLE_LOCATION,
    SAMPLE_PUBLIC_NAME,
    SAMPLE_SANGER_SAMPLE_ID,
    SAMPLE_SANGER_TAXON_ID,
    SAMPLE_SANGER_UUID,
    SAMPLE_STUDY_UUID,
    SAMPLE_VOLUME,
    SHEARED_FEMTO_FRAGMENT_SIZE,
    SHEARING_QC_COMMENTS,
    SUPPLIER_SAMPLE_NAME,
    SAMPLE_TAXON_ID,
)
from tol_lab_share.message_properties.definitions.accession_number import AccessionNumber
from tol_lab_share.message_properties.definitions.common_name import CommonName
from tol_lab_share.message_properties.definitions.concentration import Concentration
from tol_lab_share.message_properties.definitions.cost_code import CostCode
from tol_lab_share.message_properties.definitions.country_of_origin import CountryOfOrigin
from tol_lab_share.message_properties.definitions.date_utc import DateUtc
from tol_lab_share.message_properties.definitions.dict_input import dictInput
from tol_lab_share.message_properties.definitions.donor_id import DonorId
from tol_lab_share.message_properties.definitions.final_nano_drop import FinalNanoDrop
from tol_lab_share.message_properties.definitions.final_nano_drop_230 import FinalNanoDrop230
from tol_lab_share.message_properties.definitions.final_nano_drop_280 import FinalNanoDrop280
from tol_lab_share.message_properties.definitions.genome_size import GenomeSize
from tol_lab_share.message_properties.definitions.library_type import LibraryType
from tol_lab_share.message_properties.definitions.location import Location
from tol_lab_share.message_properties.definitions.post_spri_concentration import PostSPRIConcentration
from tol_lab_share.message_properties.definitions.post_spri_volume import PostSPRIVolume
from tol_lab_share.message_properties.definitions.priority_level import PriorityLevel
from tol_lab_share.message_properties.definitions.public_name import PublicName
from tol_lab_share.message_properties.definitions.sanger_sample_id import SangerSampleId
from tol_lab_share.message_properties.definitions.scientific_name_from_taxon_id import ScientificNameFromTaxonId
from tol_lab_share.message_properties.definitions.sheared_femto_fragment_size import ShearedFemtoFragmentSize
from tol_lab_share.message_properties.definitions.shearing_qc_comments import ShearingAndQCComments
from tol_lab_share.message_properties.definitions.supplier_sample_name import SupplierSampleName
from tol_lab_share.message_properties.definitions.taxon_id import TaxonId
from tol_lab_share.message_properties.definitions.uuid import Uuid
from tol_lab_share.message_properties.definitions.volume import Volume

from .message_property import MessageProperty

logger = logging.getLogger(__name__)


class Sample(MessageProperty):
    """MessageProperty that handles the parsing of a labware section for the TOL message."""

    def __init__(self, input: Any):
        super().__init__(input)

        self.add_property("cost_code", CostCode(dictInput(input, SAMPLE_COST_CODE)))
        self.add_property("study_uuid", Uuid(dictInput(input, SAMPLE_STUDY_UUID)))
        self.add_property("common_name", CommonName(dictInput(input, SAMPLE_COMMON_NAME)))
        self.add_property("concentration", Concentration(dictInput(input, SAMPLE_CONCENTRATION)))
        self.add_property("volume", Volume(dictInput(input, SAMPLE_VOLUME)))
        self.add_property(
            "country_of_origin",
            CountryOfOrigin(dictInput(input, SAMPLE_COUNTRY_OF_ORIGIN)),
        )
        self.add_property("donor_id", DonorId(dictInput(input, SAMPLE_DONOR_ID)))
        self.add_property("taxon_id", TaxonId(dictInput(input, SAMPLE_TAXON_ID)))
        self.add_property("library_type", LibraryType(dictInput(input, SAMPLE_LIBRARY_TYPE)))
        self.add_property("location", Location(dictInput(input, SAMPLE_LOCATION)))
        self.add_property("public_name", PublicName(dictInput(input, SAMPLE_PUBLIC_NAME)))
        self.add_property("sanger_sample_id", SangerSampleId(dictInput(input, SAMPLE_SANGER_SAMPLE_ID)))
        self.add_property(
            "scientific_name",
            ScientificNameFromTaxonId(TaxonId(dictInput(input, SAMPLE_SANGER_TAXON_ID))),
        )
        self.add_property("uuid", Uuid(dictInput(input, SAMPLE_SANGER_UUID)))
        self.add_property("accession_number", AccessionNumber(dictInput(input, SAMPLE_ACCESSION_NUMBER)))
        self.add_property("genome_size", GenomeSize(dictInput(input, SAMPLE_GENOME_SIZE)))
        self.add_property("collection_date", DateUtc(dictInput(input, SAMPLE_COLLECTION_DATE)))
        self.add_property("supplier_sample_name", SupplierSampleName(dictInput(input, SUPPLIER_SAMPLE_NAME)))

        self.add_property(
            "sheared_femto_fragment_size", ShearedFemtoFragmentSize(dictInput(input, SHEARED_FEMTO_FRAGMENT_SIZE))
        )
        self.add_property("post_spri_concentration", PostSPRIConcentration(dictInput(input, POST_SPRI_CONCENTRATION)))
        self.add_property("post_spri_volume", PostSPRIVolume(dictInput(input, POST_SPRI_VOLUME)))
        self.add_property("final_nano_drop_280", FinalNanoDrop280(dictInput(input, FINAL_NANODROP_280)))
        self.add_property("final_nano_drop_230", FinalNanoDrop230(dictInput(input, FINAL_NANODROP_230)))
        self.add_property("final_nano_drop", FinalNanoDrop(dictInput(input, FINAL_NANODROP)))
        self.add_property("shearing_qc_comments", ShearingAndQCComments(dictInput(input, SHEARING_QC_COMMENTS)))
        self.add_property("date_submitted_utc", DateUtc(dictInput(input, DATE_SUBMITTED_UTC)))
        self.add_property("priority_level", PriorityLevel(dictInput(input, PRIORITY_LEVEL)))
