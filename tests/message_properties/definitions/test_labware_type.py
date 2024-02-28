from tol_lab_share.message_properties.definitions.labware_type import LabwareType
from tol_lab_share.messages.properties import Value


def test_LabwareType_check_LabwareType_is_string():
    instance = LabwareType(Value(None))
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = LabwareType(Value(1234))
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = LabwareType(Value([]))
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = LabwareType(Value("1234"))
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = LabwareType(Value("plate"))
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = LabwareType(Value("Plate12x8"))
    assert instance.validate() is True
    assert len(instance.errors) == 0

    instance = LabwareType(Value("Tube"))
    assert instance.validate() is True
    assert len(instance.errors) == 0


def test_valid_locations():
    instance = LabwareType(Value("Tube"))
    assert instance.valid_locations() == []

    instance = LabwareType(Value("Plate12x8"))
    assert len(instance.valid_locations()) == 96
    assert instance.valid_locations()[95] == "H12"
    assert instance.valid_locations()[1] == "B01"
