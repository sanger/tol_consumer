from tol_lab_share import error_codes
from tol_lab_share.messages.properties.complex.labware import Labware
from tol_lab_share.messages.properties.complex.labware_type import LabwareType
from tol_lab_share.messages.properties.message_specific import CreateLabwareSample
from tol_lab_share.messages.properties.simple.value import Value


def build_sample(sample_data):
    labware = Labware(Value(None))
    sample = CreateLabwareSample(sample_data)
    lt = LabwareType(Value("Plate12x8"))

    labware.add_property("labware_type", lt)
    labware.add_property("barcode", Value("1234"))
    labware.add_property("samples", [sample])

    return sample


def check_error_is_present(sample, error_code, field):
    assert any([((x.type_id == error_code.type_id) and (x.field == field)) for x in sample.errors])


class TestSample:
    def test_validators_when_sample_is_valid(self, valid_create_labware_sample):
        instance = build_sample(valid_create_labware_sample)
        assert instance.validate() is True
        assert len(instance.errors) == 0

    def test_validators_when_sample_is_invalid(self, invalid_create_labware_sample):
        lt = LabwareType(Value("Plate12x8"))
        labware = Labware(Value("Bubidibu"))
        labware._properties["labware_type"] = lt

        instance = build_sample({"publicName": 1234})
        assert instance.validate() is False
        assert len(instance.errors) > 0

        instance = build_sample(invalid_create_labware_sample)
        assert instance.validate() is False

        check_error_is_present(instance, error_codes.ERROR_2_NOT_STRING, "common_name")
        check_error_is_present(instance, error_codes.ERROR_2_NOT_STRING, "cost_code")
        check_error_is_present(instance, error_codes.ERROR_2_NOT_STRING, "country_of_origin")
        check_error_is_present(instance, error_codes.ERROR_4_NOT_VALID_COUNTRY_INSDC, "country_of_origin")
        check_error_is_present(instance, error_codes.ERROR_2_NOT_STRING, "donor_id")
        check_error_is_present(instance, error_codes.ERROR_2_NOT_STRING, "final_nano_drop_230")
        check_error_is_present(instance, error_codes.ERROR_2_NOT_STRING, "final_nano_drop_280")
        check_error_is_present(instance, error_codes.ERROR_2_NOT_STRING, "library_type")
        check_error_is_present(instance, error_codes.ERROR_7_INVALID_LOCATION, "location")
        check_error_is_present(instance, error_codes.ERROR_2_NOT_STRING, "sanger_sample_id")
        check_error_is_present(instance, error_codes.ERROR_2_NOT_STRING, "study_uuid")
        check_error_is_present(instance, error_codes.ERROR_1_UUID_NOT_BINARY, "study_uuid")

        assert len(instance.errors) == 12
