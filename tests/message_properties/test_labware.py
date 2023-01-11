from tol_lab_share.message_properties.labware import Labware
from tol_lab_share.message_properties.input import Input


def test_labware_is_valid():
    labware = {
        "labwareType": "Plate12x8",
        "labwareUuid": "dd490ee5-fd1d-456d-99fd-eb9d3861e0f9".encode(),
        "barcode": "BARCODE001",
        "samples": [],
    }

    instance = Labware(Input(labware))
    assert instance.validate() is True
    assert len(instance.errors) == 0


def test_sample_is_invalid():
    labware = {
        "labwareType": "Plate12x9",
        "labwareUuid": "dd490ee5-fd1d-456d-99fd-eb9d3861e0f9",
        "barcode": 1234,
        "samples": [],
    }

    instance = Labware(Input(labware))
    assert instance.validate() is False
    assert len(instance.errors) == 4

    labware = {
        "labwareType": "Plate12x8",
        "labwareUuid": "dd490ee5-fd1d-456d-99fd-eb9d3861e0f9".encode(),
        "samples": [],
    }
    instance = Labware(Input(labware))
    assert instance.validate() is False
    assert len(instance.errors) == 1
