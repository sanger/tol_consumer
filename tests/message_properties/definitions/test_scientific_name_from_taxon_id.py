from tol_lab_share.message_properties.definitions.scientific_name_from_taxon_id import ScientificNameFromTaxonId
from tol_lab_share.messages.properties import Value
from tol_lab_share.error_codes import ExceptionErrorCode
from helpers import check_validates_integer_string
import requests_mock
import pytest


def reset_taxon_id_cache():
    ScientificNameFromTaxonId.reset_cache()


def test_ScientificNameFromTaxonId_check_ScientificNameFromTaxonId_is_int():
    check_validates_integer_string(ScientificNameFromTaxonId)


def test_can_access_external_service(config, taxonomy_record):
    reset_taxon_id_cache()
    with requests_mock.Mocker() as m:
        m.get(config.EBI_TAXONOMY_URL + "/9600", json=taxonomy_record)
        instance = ScientificNameFromTaxonId(Value("9600"))
        assert instance.value == "Pongo pygmaeus"


def test_can_handle_fail(config):
    reset_taxon_id_cache()
    with requests_mock.Mocker() as m:
        m.get(config.EBI_TAXONOMY_URL + "/9600", json="", status_code=404)
        instance = ScientificNameFromTaxonId(Value("9600"))
        with pytest.raises(ExceptionErrorCode):
            instance.value


def test_can_retrieve_from_cache(config, taxonomy_record):
    reset_taxon_id_cache()
    with requests_mock.Mocker() as m:
        m.register_uri(
            "GET",
            config.EBI_TAXONOMY_URL + "/9600",
            [{"json": taxonomy_record, "status_code": 200}, {"json": {}, "status_code": 500}],
        )
        instance = ScientificNameFromTaxonId(Value("9600"))
        assert instance.value == "Pongo pygmaeus"

        assert instance.value == "Pongo pygmaeus"
        instance2 = ScientificNameFromTaxonId(Value("9600"))
        assert instance2.value == "Pongo pygmaeus"


def test_can_reset_cache(config, taxonomy_record):
    reset_taxon_id_cache()
    with requests_mock.Mocker() as m:
        m.register_uri(
            "GET",
            config.EBI_TAXONOMY_URL + "/9600",
            [
                {"json": taxonomy_record, "status_code": 200},
                {"json": {}, "status_code": 500},
                {"json": taxonomy_record, "status_code": 200},
            ],
        )
        instance = ScientificNameFromTaxonId(Value("9600"))
        assert instance.value == "Pongo pygmaeus"

        reset_taxon_id_cache()
        assert instance.value == "Pongo pygmaeus"

        instance2 = ScientificNameFromTaxonId(Value("9600"))
        with pytest.raises(ExceptionErrorCode):
            instance2.value

        reset_taxon_id_cache()
        instance3 = ScientificNameFromTaxonId(Value("9600"))
        assert instance3.value == "Pongo pygmaeus"
