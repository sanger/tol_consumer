from tol_lab_share.message_properties.definitions.sample import Sample
from tol_lab_share.message_properties.definitions.labware_type import LabwareType
from tol_lab_share.message_properties.definitions.labware import Labware
from tol_lab_share.message_properties.definitions.input import Input


def build_sample(sample_data):
    labware = Labware(Input(None))
    sample = Sample(sample_data)
    lt = LabwareType(Input("Plate12x8"))

    labware.add_property("labware_type", lt)
    labware.add_property("samples", [sample])

    return sample


def test_sample_is_valid(valid_sample):
    instance = build_sample(valid_sample)
    assert instance.validate() is True
    assert len(instance.errors) == 0


def test_sample_is_invalid(invalid_sample):
    lt = LabwareType(Input("Plate12x8"))
    labware = Labware(Input("Bubidibu"))
    labware._properties["labware_type"] = lt

    instance = build_sample({"publicName": 1234})
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = build_sample(invalid_sample)
    assert instance.validate() is False
    assert len(instance.errors) > 0
