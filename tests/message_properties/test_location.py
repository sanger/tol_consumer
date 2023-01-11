from tol_lab_share.message_properties.location import Location
from tol_lab_share.message_properties.labware_type import LabwareType
from tol_lab_share.message_properties.labware import Labware
from tol_lab_share.message_properties.input import Input


def test_Location_with_wrong_labware_type():
    labware = Labware(Input(None))
    lt = LabwareType(Input(None))
    labware._properties["labware_type"] = lt

    instance = Location("A01", labware)
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = Location(None, labware)
    assert instance.validate() is False
    assert len(instance.errors) > 0


def test_Location_check_Location_when_plate12x8():
    labware = Labware(Input(None))
    lt = LabwareType(Input("Plate12x8"))
    labware._properties["labware_type"] = lt

    instance = Location(Input(None), labware)
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = Location(Input(1234), labware)
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = Location(Input([]), labware)
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = Location(Input("1234"), labware)
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = Location(Input("a01"), labware)
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = Location(Input("N01"), labware)
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = Location(Input("A1"), labware)
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = Location(Input("A01"), labware)
    assert instance.validate() is True
    assert len(instance.errors) == 0

    instance = Location(Input("A12"), labware)
    assert instance.validate() is True
    assert len(instance.errors) == 0


def test_Location_check_Location_when_tube():
    labware = Labware(Input(None))
    labware_type = LabwareType(Input("Tube"))
    labware._properties["labware_type"] = labware_type

    instance = Location(Input(1234), labware)
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = Location(Input([]), labware)
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = Location(Input("1234"), labware)
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = Location(Input("a01"), labware)
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = Location(Input("N01"), labware)
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = Location(Input("A1"), labware)
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = Location(Input("A01"), labware)
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = Location(Input("A12"), labware)
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = Location(Input(None), labware)
    assert instance.validate() is True
    assert len(instance.errors) == 0
