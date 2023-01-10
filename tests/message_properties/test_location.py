from tol_lab_share.message_properties.location import Location
from tol_lab_share.message_properties.labware_type import LabwareType
from tol_lab_share.message_properties.input import Input


def test_Location_with_wrong_labware_type():
    instance = Location(LabwareType(Input(None)), "A01")
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = Location(LabwareType(Input(None)), None)
    assert instance.validate() is False
    assert len(instance.errors) > 0


def test_Location_check_Location_when_plate12x8():
    labware_type = LabwareType(Input("Plate12x8"))
    instance = Location(labware_type, Input(None))
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = Location(labware_type, Input(1234))
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = Location(labware_type, Input([]))
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = Location(labware_type, Input("1234"))
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = Location(labware_type, Input("a01"))
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = Location(labware_type, Input("N01"))
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = Location(labware_type, Input("A1"))
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = Location(labware_type, Input("A01"))
    assert instance.validate() is True
    assert len(instance.errors) == 0

    instance = Location(labware_type, Input("A12"))
    assert instance.validate() is True
    assert len(instance.errors) == 0


def test_Location_check_Location_when_tube():
    labware_type = LabwareType(Input("Tube"))

    instance = Location(labware_type, Input(1234))
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = Location(labware_type, Input([]))
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = Location(labware_type, Input("1234"))
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = Location(labware_type, Input("a01"))
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = Location(labware_type, Input("N01"))
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = Location(labware_type, Input("A1"))
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = Location(labware_type, Input("A01"))
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = Location(labware_type, Input("A12"))
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = Location(labware_type, Input(None))
    assert instance.validate() is True
    assert len(instance.errors) == 0
