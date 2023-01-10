from tol_lab_share.message_properties.location import Location
from tol_lab_share.message_properties.labware_type import LabwareType


def test_Location_with_wrong_labware_type():
    instance = Location(LabwareType(None), "A01")
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = Location(LabwareType(None), None)
    assert instance.validate() is False
    assert len(instance.errors) > 0


def test_Location_check_Location_when_plate12x8():
    labware_type = LabwareType("Plate12x8")
    instance = Location(labware_type, None)
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = Location(labware_type, 1234)
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = Location(labware_type, [])
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = Location(labware_type, "1234")
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = Location(labware_type, "a01")
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = Location(labware_type, "N01")
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = Location(labware_type, "A1")
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = Location(labware_type, "A01")
    assert instance.validate() is True
    assert len(instance.errors) == 0

    instance = Location(labware_type, "A12")
    assert instance.validate() is True
    assert len(instance.errors) == 0


def test_Location_check_Location_when_tube():
    labware_type = LabwareType("Tube")

    instance = Location(labware_type, 1234)
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = Location(labware_type, [])
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = Location(labware_type, "1234")
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = Location(labware_type, "a01")
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = Location(labware_type, "N01")
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = Location(labware_type, "A1")
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = Location(labware_type, "A01")
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = Location(labware_type, "A12")
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = Location(labware_type, None)
    assert instance.validate() is True
    assert len(instance.errors) == 0
