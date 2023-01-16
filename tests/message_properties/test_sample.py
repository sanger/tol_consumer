from tol_lab_share.message_properties.sample import Sample
from tol_lab_share.message_properties.labware_type import LabwareType
from tol_lab_share.message_properties.labware import Labware
from tol_lab_share.message_properties.input import Input


def test_sample_is_valid(valid_sample):
    lt = LabwareType(Input("Plate12x8"))

    labware = Labware(Input("Bubidibu"))
    labware._properties["labware_type"] = lt

    instance = Sample(valid_sample, labware, 0)
    assert instance.validate() is True
    assert len(instance.errors) == 0


def test_sample_is_invalid(invalid_sample):
    lt = LabwareType(Input("Plate12x8"))
    labware = Labware(Input("Bubidibu"))
    labware._properties["labware_type"] = lt

    instance = Sample({"publicName": 1234}, labware, 0)
    assert instance.validate() is False
    assert len(instance.errors) > 0

    labware = Labware(Input("Bubidibu"))
    labware._properties["labware_type"] = lt

    instance = Sample(invalid_sample, labware, 0)
    assert instance.validate() is False
    assert len(instance.errors) > 0
