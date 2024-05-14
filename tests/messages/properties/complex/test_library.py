import pytest
from tol_lab_share import error_codes
from tol_lab_share.messages.properties.complex.library import Library
from tol_lab_share.messages.properties.simple import Value
from tol_lab_share.messages.traction.reception_message import TractionReceptionMessageRequest


@pytest.fixture
def valid_library(request):
    return Value(
        {
            "volume": 123.45,
            "concentration": 345.678901,
            "boxBarcode": "BoxBarcode123",
            **request.param,
        }
    )


@pytest.fixture
def invalid_library():
    return Value(
        {
            "volume": "NotAFloat",
            "concentration": 1234,  # Also not a float
        }
    )


def check_error_is_present(sample, error_code, field):
    assert any(
        [((x.type_id == error_code.type_id) and (x.field == field)) for x in sample.errors]
    ), f"Error type '{error_code.type_id}' for field '{field}' not found among {sample.errors}"


class TestBioscanPoolXpSample:
    # Note: Although we test negative numbers for insertSize, Traction would not accept them.
    #       It is not our responsibility to validate that the recipient of this data would find it acceptable.
    @pytest.mark.parametrize(
        "valid_library",
        [{}, {"insertSize": -50}, {"insertSize": 0}, {"insertSize": 50}],
        ids=["no insertSize", "insertSize=-50", "insertSize=0", "insertSize=50"],
        indirect=True,
    )
    def test_validates_true_when_library_is_valid(self, valid_library):
        instance = Library(valid_library)
        assert instance.validate() is True
        assert len(instance.errors) == 0

    def test_validates_false_when_request_incomplete(self):
        instance = Library(Value({}))
        assert instance.validate() is False
        assert len(instance.errors) > 0

    def test_validates_false_when_request_is_invalid(self, invalid_library):
        instance = Library(invalid_library)
        assert instance.validate() is False

        check_error_is_present(instance, error_codes.ERROR_5_NOT_FLOAT, "volume")
        check_error_is_present(instance, error_codes.ERROR_5_NOT_FLOAT, "concentration")
        check_error_is_present(instance, error_codes.ERROR_9_INVALID_INPUT, "box_barcode")

        assert len(instance.errors) == 3

    @pytest.mark.parametrize(
        "valid_library",
        [{}, {"insertSize": -50}, {"insertSize": 0}, {"insertSize": 50}],
        ids=["no insertSize", "insertSize=-50", "insertSize=0", "insertSize=50"],
        indirect=True,
    )
    def test_add_to_message_property_for_traction_reception_message_request(self, valid_library):
        instance = Library(valid_library)

        request = TractionReceptionMessageRequest()
        instance.add_to_message_property(request)

        assert request.library_volume == 123.45
        assert request.library_concentration == 345.678901
        assert request.template_prep_kit_box_barcode == "BoxBarcode123"
        assert request.library_insert_size == valid_library.value.get("insertSize", None)
