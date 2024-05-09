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
from ..complex.country_of_origin import CountryOfOrigin
from ..complex.date_utc import DateUtc
from ..complex.location import Location
from ..complex.scientific_name_from_taxon_id import ScientificNameFromTaxonId
from ..complex.uuid import Uuid
from ..simple.dict_value import DictValue
from ..simple.string_value import StringValue

from tol_lab_share.messages.properties import MessageProperty

logger = logging.getLogger(__name__)


class CreateLabwareSample(MessageProperty):
    """MessageProperty that handles the parsing of a labware section for the TOL message."""

    def __init__(self, input: Any):
        super().__init__(input)

        self.add_property("accession_number", StringValue(DictValue(input, SAMPLE_ACCESSION_NUMBER)))
        self.add_property("collection_date", DateUtc(DictValue(input, SAMPLE_COLLECTION_DATE)))
        self.add_property("common_name", StringValue(DictValue(input, SAMPLE_COMMON_NAME)))
        self.add_property("concentration", StringValue(DictValue(input, SAMPLE_CONCENTRATION)))
        self.add_property("cost_code", StringValue(DictValue(input, SAMPLE_COST_CODE)))
        self.add_property("country_of_origin", CountryOfOrigin(DictValue(input, SAMPLE_COUNTRY_OF_ORIGIN)))
        self.add_property("date_submitted_utc", DateUtc(DictValue(input, DATE_SUBMITTED_UTC)))
        self.add_property("donor_id", StringValue(DictValue(input, SAMPLE_DONOR_ID)))
        self.add_property("final_nano_drop_230", StringValue(DictValue(input, FINAL_NANODROP_230)))
        self.add_property("final_nano_drop_280", StringValue(DictValue(input, FINAL_NANODROP_280)))
        self.add_property("final_nano_drop", StringValue(DictValue(input, FINAL_NANODROP)))
        self.add_property("genome_size", StringValue(DictValue(input, SAMPLE_GENOME_SIZE)))
        self.add_property("library_type", StringValue(DictValue(input, SAMPLE_LIBRARY_TYPE)))
        self.add_property("location", Location(DictValue(input, SAMPLE_LOCATION)))
        self.add_property("post_spri_concentration", StringValue(DictValue(input, POST_SPRI_CONCENTRATION)))
        self.add_property("post_spri_volume", StringValue(DictValue(input, POST_SPRI_VOLUME)))
        self.add_property("priority_level", StringValue(DictValue(input, PRIORITY_LEVEL)))
        self.add_property("public_name", StringValue(DictValue(input, SAMPLE_PUBLIC_NAME)))
        self.add_property("sanger_sample_id", StringValue(DictValue(input, SAMPLE_SANGER_SAMPLE_ID)))
        self.add_property(
            "scientific_name", ScientificNameFromTaxonId(StringValue(DictValue(input, SAMPLE_SANGER_TAXON_ID)))
        )
        self.add_property("sheared_femto_fragment_size", StringValue(DictValue(input, SHEARED_FEMTO_FRAGMENT_SIZE)))
        self.add_property("shearing_qc_comments", StringValue(DictValue(input, SHEARING_QC_COMMENTS)))
        self.add_property("study_uuid", Uuid(DictValue(input, SAMPLE_STUDY_UUID)))
        self.add_property("supplier_sample_name", StringValue(DictValue(input, SUPPLIER_SAMPLE_NAME)))
        self.add_property("taxon_id", StringValue(DictValue(input, SAMPLE_TAXON_ID)))
        self.add_property("uuid", Uuid(DictValue(input, SAMPLE_SANGER_UUID)))
        self.add_property("volume", StringValue(DictValue(input, SAMPLE_VOLUME)))
