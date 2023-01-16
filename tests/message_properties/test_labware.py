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


def test_count_of_total_samples(valid_sample):
    labware = {
        "labwareType": "Plate12x8",
        "labwareUuid": "dd490ee5-fd1d-456d-99fd-eb9d3861e0f9",
        "barcode": 1234,
        "samples": [],
    }

    instance = Labware(Input(labware))
    assert instance.count_of_total_samples() == 0

    labware2 = {
        "labwareType": "Plate12x8",
        "labwareUuid": "dd490ee5-fd1d-456d-99fd-eb9d3861e0f9",
        "barcode": 1234,
        "samples": [valid_sample, valid_sample],
    }

    instance = Labware(Input(labware2))
    assert instance.count_of_total_samples() == 2


def test_count_of_valid_samples(valid_sample, invalid_sample):
    labware = {
        "labwareType": "Plate12x8",
        "labwareUuid": "dd490ee5-fd1d-456d-99fd-eb9d3861e0f9",
        "barcode": 1234,
        "samples": [],
    }

    instance = Labware(Input(labware))
    instance.validate()
    assert instance.count_of_valid_samples() == 0

    labware2 = {
        "labwareType": "Plate12x8",
        "labwareUuid": "dd490ee5-fd1d-456d-99fd-eb9d3861e0f9",
        "barcode": 1234,
        "samples": [valid_sample, valid_sample],
    }

    instance = Labware(Input(labware2))
    instance.validate()
    assert instance.count_of_valid_samples() == 2

    labware2 = {
        "labwareType": "Plate12x8",
        "labwareUuid": "dd490ee5-fd1d-456d-99fd-eb9d3861e0f9",
        "barcode": 1234,
        "samples": [invalid_sample, valid_sample],
    }

    instance = Labware(Input(labware2))
    instance.validate()
    assert instance.count_of_valid_samples() == 1
