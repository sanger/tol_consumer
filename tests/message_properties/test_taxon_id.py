from tol_lab_share.message_properties.taxon_id import TaxonId
from tol_lab_share.message_properties.input import Input
from tol_lab_share.message_properties.message_property import ExceptionMessageProperty
from helpers import check_validates_integer
import requests_mock
import pytest


def reset_taxon_id_cache():
    TaxonId.reset_cache()


def test_TaxonId_check_TaxonId_is_int():
    check_validates_integer(TaxonId)


def test_can_access_external_service(config, taxonomy_record):
    reset_taxon_id_cache()
    with requests_mock.Mocker() as m:
        m.get(config.EBI_TAXONOMY_URL + "/9600", json=taxonomy_record)
        instance = TaxonId(Input(9600))
        assert instance.value == "Pongo pygmaeus"


def test_can_handle_fail(config):
    reset_taxon_id_cache()
    with requests_mock.Mocker() as m:
        m.get(config.EBI_TAXONOMY_URL + "/9600", json="", status_code=404)
        instance = TaxonId(Input(9600))
        with pytest.raises(ExceptionMessageProperty):
            instance.value


def test_can_retrieve_from_cache(config, taxonomy_record):
    reset_taxon_id_cache()
    with requests_mock.Mocker() as m:
        m.register_uri(
            "GET",
            config.EBI_TAXONOMY_URL + "/9600",
            [{"json": taxonomy_record, "status_code": 200}, {"json": {}, "status_code": 500}],
        )
        instance = TaxonId(Input(9600))
        assert instance.value == "Pongo pygmaeus"

        assert instance.value == "Pongo pygmaeus"
        instance2 = TaxonId(Input(9600))
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
        instance = TaxonId(Input(9600))
        assert instance.value == "Pongo pygmaeus"

        reset_taxon_id_cache()
        assert instance.value == "Pongo pygmaeus"

        instance2 = TaxonId(Input(9600))
        with pytest.raises(ExceptionMessageProperty):
            instance2.value

        reset_taxon_id_cache()
        instance3 = TaxonId(Input(9600))
        assert instance3.value == "Pongo pygmaeus"
