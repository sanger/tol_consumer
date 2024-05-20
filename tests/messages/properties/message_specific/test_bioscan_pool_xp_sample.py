import pytest
from tol_lab_share import error_codes
from tol_lab_share.messages.properties.message_specific.bioscan_pool_xp_sample import BioscanPoolXpSample
from tol_lab_share.messages.properties.simple.dict_value import Value
from tol_lab_share.messages.traction.reception_message import TractionReceptionMessageRequest


@pytest.fixture
def valid_sample():
    return Value(
        {
            "sampleName": "ValidSample",
            "sampleUuid": b"12345678-1234-1234-1234-1234567890ab",
            "speciesName": "ValidSpecies",
        }
    )


@pytest.fixture
def invalid_sample():
    # Sample is invalid because:
    # - sampleName is not a string
    # - sampleUuid is not binary data
    # - speciesName is not optional but missing
    return Value(
        {
            "sampleName": 42,
            "sampleUuid": "12345678-1234-1234-1234-1234567890ab",
        }
    )


def check_error_is_present(sample, error_code, field):
    assert any(
        [((x.type_id == error_code.type_id) and (x.field == field)) for x in sample.errors]
    ), f"Error type '{error_code.type_id}' for field '{field}' not found among {sample.errors}"


class TestBioscanPoolXpSample:
    def test_validators_when_sample_is_valid(self, valid_sample):
        instance = BioscanPoolXpSample(valid_sample)
        assert instance.validate() is True
        assert len(instance.errors) == 0

    def test_validators_when_sample_incomplete(self):
        instance = BioscanPoolXpSample(Value({"sampleName": "IncompleteSample"}))
        assert instance.validate() is False
        assert len(instance.errors) > 0

    def test_validators_when_sample_is_invalid(self, invalid_sample):
        instance = BioscanPoolXpSample(invalid_sample)
        assert instance.validate() is False

        check_error_is_present(instance, error_codes.ERROR_2_NOT_STRING, "name")
        check_error_is_present(instance, error_codes.ERROR_1_UUID_NOT_BINARY, "uuid")
        check_error_is_present(instance, error_codes.ERROR_2_UUID_NOT_RIGHT_FORMAT, "uuid")
        check_error_is_present(instance, error_codes.ERROR_9_INVALID_INPUT, "species_name")

        assert len(instance.errors) == 4

    def test_add_to_message_property_for_traction_reception_message_request(self, valid_sample):
        instance = BioscanPoolXpSample(valid_sample)

        request = TractionReceptionMessageRequest()
        instance.add_to_message_property(request)

        assert request.sample_name == "ValidSample"
        assert request.sample_uuid == "12345678-1234-1234-1234-1234567890ab"
        assert request.species == "ValidSpecies"
