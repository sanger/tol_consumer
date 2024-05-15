import pytest
from tol_lab_share import error_codes
from tol_lab_share.messages.properties.complex.request import Request
from tol_lab_share.messages.properties.simple import Value


@pytest.fixture
def valid_request(request):
    return Value(
        {
            "costCode": "CostCode789",
            "libraryType": "LibraryType123",
            "studyUuid": b"12345678-1234-1234-1234-1234567890ab",
            **request.param,
        }
    )


@pytest.fixture
def invalid_request():
    # Request is invalid because:
    # - costCode is not a string
    # - libraryType is not optional but missing
    # - studyUuid is not binary data
    return Value(
        {
            "costCode": 1234,
            "studyUuid": "12345678-1234-1234-1234-1234567890ab",
        }
    )


def check_error_is_present(sample, error_code, field):
    assert any(
        [((x.type_id == error_code.type_id) and (x.field == field)) for x in sample.errors]
    ), f"Error type '{error_code.type_id}' for field '{field}' not found among {sample.errors}"


class TestBioscanPoolXpSample:
    @pytest.mark.parametrize(
        "valid_request", [{}, {"genomeSize": ""}, {"genomeSize": "1,234,567,890 bp"}], indirect=True
    )
    def test_validators_when_request_is_valid(self, valid_request):
        instance = Request(valid_request)
        assert instance.validate() is True
        assert len(instance.errors) == 0

    def test_validators_when_request_incomplete(self):
        instance = Request(Value({}))
        assert instance.validate() is False
        assert len(instance.errors) > 0

    def test_validators_when_request_is_invalid(self, invalid_request):
        instance = Request(invalid_request)
        assert instance.validate() is False

        check_error_is_present(instance, error_codes.ERROR_2_NOT_STRING, "cost_code")
        check_error_is_present(instance, error_codes.ERROR_9_INVALID_INPUT, "library_type")
        check_error_is_present(instance, error_codes.ERROR_1_UUID_NOT_BINARY, "study_uuid")
        check_error_is_present(instance, error_codes.ERROR_2_UUID_NOT_RIGHT_FORMAT, "study_uuid")

        assert len(instance.errors) == 4
