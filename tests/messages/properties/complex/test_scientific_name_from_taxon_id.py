import requests_mock
import pytest

from tol_lab_share.messages.properties.complex import ScientificNameFromTaxonId
from tol_lab_share.messages.properties.simple import Value
from tol_lab_share.error_codes import ExceptionErrorCode
from tests.messages.properties.helpers import check_validates_string


def reset_cache():
    ScientificNameFromTaxonId.reset_cache()


class TestScientificNameFromTaxonId:
    def test_validators_behave_correctly(self):
        check_validates_string(ScientificNameFromTaxonId)

    def test_gets_taxon_id_from_ebi(self, config, taxonomy_record):
        reset_cache()
        with requests_mock.Mocker() as m:
            m.get(config.EBI_TAXONOMY_URL + "/9600", json=taxonomy_record)
            instance = ScientificNameFromTaxonId(Value("9600"))
            assert instance.value == "Pongo pygmaeus"

    def test_handles_failed_get_from_ebi(self, config):
        reset_cache()
        with requests_mock.Mocker() as m:
            m.get(config.EBI_TAXONOMY_URL + "/9600", json="", status_code=404)
            instance = ScientificNameFromTaxonId(Value("9600"))
            with pytest.raises(ExceptionErrorCode):
                instance.value

    def test_retrieves_previous_value_from_cache(self, config, taxonomy_record):
        reset_cache()
        with requests_mock.Mocker() as m:
            m.get(
                config.EBI_TAXONOMY_URL + "/9600",
                [{"json": taxonomy_record, "status_code": 200}, {"json": {}, "status_code": 500}],
            )

            instance = ScientificNameFromTaxonId(Value("9600"))
            assert instance.value == "Pongo pygmaeus"  # This is the first time the value is retrieved.
            assert instance.value == "Pongo pygmaeus"  # This must be using the cache, otherwise it would fail.

            instance2 = ScientificNameFromTaxonId(Value("9600"))
            assert instance2.value == "Pongo pygmaeus"  # This must be using the cache, otherwise it would fail.

    def test_can_reset_cache(self, config, taxonomy_record):
        reset_cache()
        with requests_mock.Mocker() as m:
            m.get(
                config.EBI_TAXONOMY_URL + "/9600",
                [
                    {"json": taxonomy_record, "status_code": 200},
                    {"json": {}, "status_code": 500},
                    {"json": taxonomy_record, "status_code": 200},
                ],
            )
            instance = ScientificNameFromTaxonId(Value("9600"))
            assert instance.value == "Pongo pygmaeus"

            reset_cache()
            assert instance.value == "Pongo pygmaeus"

            instance2 = ScientificNameFromTaxonId(Value("9600"))
            with pytest.raises(ExceptionErrorCode):
                instance2.value

            reset_cache()
            instance3 = ScientificNameFromTaxonId(Value("9600"))
            assert instance3.value == "Pongo pygmaeus"
