from tol_lab_share.message_properties.definitions.location import Location
from tol_lab_share.message_properties.definitions.labware_type import LabwareType
from tol_lab_share.message_properties.definitions.labware import Labware
from tol_lab_share.messages.properties import Value


def build_location(location_data, labware_type_data):
    labware = Labware(Value(None))
    sample = Value(None)
    lt = LabwareType(Value(labware_type_data))
    labware.add_property("labware_type", lt)
    labware.add_property("samples", [sample])

    instance = Location(Value(location_data))
    sample.add_property("location", instance)

    return instance


def test_Location_with_wrong_labware_type():
    instance = build_location("A01", None)

    assert instance.validate() is False
    assert len(instance.errors) > 0


def test_location_with_wrong_location_info():
    instance = build_location(None, "Plate12x8")

    assert instance.validate() is False
    assert len(instance.errors) > 0


def test_location_check_Location_when_plate12x8():
    instance = build_location(None, "Plate12x8")
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = build_location(1234, "Plate12x8")
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = build_location([], "Plate12x8")
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = build_location("1234", "Plate12x8")
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = build_location("a01", "Plate12x8")
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = build_location("N01", "Plate12x8")
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = build_location("A1", "Plate12x8")
    assert instance.validate() is True
    assert len(instance.errors) == 0

    instance = build_location("A01", "Plate12x8")
    assert instance.validate() is True
    assert len(instance.errors) == 0

    instance = build_location("A12", "Plate12x8")
    assert instance.validate() is True
    assert len(instance.errors) == 0


def test_Location_check_Location_when_tube():
    instance = build_location(1234, "Tube")
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = build_location([], "Tube")
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = build_location("1234", "Tube")
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = build_location("a01", "Tube")
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = build_location("N01", "Tube")
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = build_location("A1", "Tube")
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = build_location("A01", "Tube")
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = build_location("A12", "Tube")
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = build_location(None, "Tube")
    assert instance.validate() is True
    assert len(instance.errors) == 0


def test_location_value():
    instance = build_location(None, "Tube")
    assert instance.value is None
    instance = build_location("A01", "Plate12x8")
    assert instance.value == "A1"


def test_location_padded():
    instance = build_location("A1", "Plate12x8")
    assert instance.padded() == "A01"

    instance = build_location("A01", "Plate12x8")
    assert instance.padded() == "A01"

    instance = build_location("A12", "Plate12x8")
    assert instance.padded() == "A12"

    instance = build_location("A233", "Plate12x8")
    assert instance.padded() == "A233"

    instance = build_location(None, "Tube")
    assert instance.padded() is None


def test_location_unpadded():
    instance = build_location("A1", "Plate12x8")
    assert instance.unpadded() == "A1"

    instance = build_location("A01", "Plate12x8")
    assert instance.unpadded() == "A1"

    instance = build_location("A12", "Plate12x8")
    assert instance.unpadded() == "A12"

    instance = build_location("A233", "Plate12x8")
    assert instance.unpadded() == "A233"

    instance = build_location(None, "Tube")
    assert instance.unpadded() is None
