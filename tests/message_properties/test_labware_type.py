from tol_lab_share.message_properties.labware_type import LabwareType


def test_LabwareType_check_LabwareType_is_string():
    instance = LabwareType(None)
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = LabwareType(1234)
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = LabwareType([])
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = LabwareType("1234")
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = LabwareType("plate")
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = LabwareType("Plate12x8")
    assert instance.validate() is True
    assert len(instance.errors) == 0

    instance = LabwareType("Tube")
    assert instance.validate() is True
    assert len(instance.errors) == 0


def test_valid_locations():
    instance = LabwareType("Tube")
    assert instance.valid_locations() == []

    instance = LabwareType("Plate12x8")
    assert len(instance.valid_locations()) == 96
    assert instance.valid_locations()[95] == "H12"
    assert instance.valid_locations()[1] == "B01"
