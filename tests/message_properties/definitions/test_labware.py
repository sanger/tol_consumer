from tol_lab_share.message_properties.definitions.input import Input
from tol_lab_share.message_properties.definitions.labware import Labware
from tol_lab_share.message_properties.definitions.location import Location
from tol_lab_share.traction.output_traction_message import OutputTractionMessage
from tol_lab_share.messages.traction_qc_message import TractionQcMessage


def test_labware_is_valid():
    labware = {
        "labwareType": "Plate12x8",
        "labwareUuid": "dd490ee5-fd1d-456d-99fd-eb9d3861e0f9".encode(),
        "barcode": "BARCODE001",
        "samples": [],
    }

    instance = Labware(Input(labware))
    assert instance.validate() is True
    assert instance.errors == []


def test_sample_is_invalid():
    labware = {
        "labwareType": "Plate12x9",
        "labwareUuid": "dd490ee5-fd1d-456d-99fd-eb9d3861e0f9",
        "barcode": 1234,
        "samples": [],
    }

    instance = Labware(Input(labware))
    assert instance.validate() is False
    assert len(instance.errors) > 0

    labware = {
        "labwareType": "Plate12x8",
        "labwareUuid": "dd490ee5-fd1d-456d-99fd-eb9d3861e0f9".encode(),
        "samples": [],
    }
    instance = Labware(Input(labware))
    assert instance.validate() is False
    assert len(instance.errors) > 0


def test_count_of_total_samples(valid_sample):
    labware = {
        "labwareType": "Plate12x8",
        "labwareUuid": "dd490ee5-fd1d-456d-99fd-eb9d3861e0f9".encode(),
        "barcode": "1234",
        "samples": [],
    }

    instance = Labware(Input(labware))
    assert instance.validate()
    assert instance.count_of_total_samples() == 0

    labware2 = {
        "labwareType": "Plate12x8",
        "labwareUuid": "dd490ee5-fd1d-456d-99fd-eb9d3861e0f9".encode(),
        "barcode": "1234",
        "samples": [valid_sample, valid_sample],
    }

    instance = Labware(Input(labware2))
    assert instance.validate()
    assert instance.count_of_total_samples() == 2
    assert instance.errors == []


def test_count_of_valid_samples(valid_sample, invalid_sample):
    labware = {
        "labwareType": "Plate12x8",
        "labwareUuid": b"dd490ee5-fd1d-456d-99fd-eb9d3861e0f9",
        "barcode": "1234",
        "samples": [],
    }

    instance = Labware(Input(labware))
    instance.validate()
    assert instance.count_of_valid_samples() == 0

    labware2 = {
        "labwareType": "Plate12x8",
        "labwareUuid": b"dd490ee5-fd1d-456d-99fd-eb9d3861e0f9",
        "barcode": "1234",
        "samples": [valid_sample, valid_sample],
    }

    instance = Labware(Input(labware2))
    instance.validate()
    assert instance.errors == []
    assert instance.count_of_valid_samples() == 2

    labware2 = {
        "labwareType": "Plate12x8",
        "labwareUuid": b"dd490ee5-fd1d-456d-99fd-eb9d3861e0f9",
        "barcode": "1234",
        "samples": [invalid_sample, valid_sample],
    }

    instance = Labware(Input(labware2))
    instance.validate()
    assert instance.count_of_valid_samples() == 1


def test_labware_add_to_message_wells(valid_sample):
    data = {
        "labwareType": "Plate12x8",
        "labwareUuid": "dd490ee5-fd1d-456d-99fd-eb9d3861e0f9".encode(),
        "barcode": "BARCODE001",
        "samples": [valid_sample],
    }
    instance = Labware(Input(data))
    assert instance.validate()

    traction_message = OutputTractionMessage()
    instance.add_to_message_property(traction_message)

    assert traction_message._requests[0].study_uuid == "dd490ee5-fd1d-456d-99fd-eb9d3861e014"
    assert traction_message._requests[0].sample_name == "cichlid_pacbio8196429"
    assert traction_message._requests[0].public_name == "SamplePublicName1"
    assert traction_message._requests[0].sanger_sample_id == "cichlid_pacbio8196429"
    assert traction_message._requests[0].sample_uuid == "dd490ee5-fd1d-456d-99fd-eb9d3861e0f6"
    assert traction_message._requests[0].library_type == "Library1"
    assert traction_message._requests[0].species == "Mus musculus"
    assert traction_message._requests[0].container_barcode == "BARCODE001"
    assert traction_message._requests[0].container_location == "A1"
    assert traction_message._requests[0].container_type == "wells"
    assert traction_message._requests[0].cost_code == "S1234"


def test_labware_add_to_message_tubes(valid_sample):
    data = {
        "labwareType": "Tube",
        "labwareUuid": "dd490ee5-fd1d-456d-99fd-eb9d3861e0f9".encode(),
        "barcode": "BARCODE001",
        "samples": [valid_sample],
    }
    instance = Labware(Input(data))

    traction_message = OutputTractionMessage()
    instance.add_to_message_property(traction_message)

    assert traction_message._requests[0].study_uuid == "dd490ee5-fd1d-456d-99fd-eb9d3861e014"
    assert traction_message._requests[0].sample_name == "cichlid_pacbio8196429"
    assert traction_message._requests[0].sanger_sample_id == "cichlid_pacbio8196429"
    assert traction_message._requests[0].public_name == "SamplePublicName1"
    assert traction_message._requests[0].sample_uuid == "dd490ee5-fd1d-456d-99fd-eb9d3861e0f6"
    assert traction_message._requests[0].library_type == "Library1"
    assert traction_message._requests[0].species == "Mus musculus"
    assert traction_message._requests[0].container_barcode == "BARCODE001"
    assert traction_message._requests[0].container_location == "A1"
    assert traction_message._requests[0].container_type == "tubes"
    assert traction_message._requests[0].cost_code == "S1234"


def test_labware_add_to_message_uses_unpadded_location(valid_sample):
    data = {
        "labwareType": "Plate12x8",
        "labwareUuid": "dd490ee5-fd1d-456d-99fd-eb9d3861e0f9".encode(),
        "barcode": "BARCODE001",
        "samples": [valid_sample],
    }
    instance = Labware(Input(data))
    instance.properties("samples")[0].add_property("location", Location(Input("B01")))
    traction_message = OutputTractionMessage()
    instance.add_to_message_property(traction_message)
    assert traction_message._requests[0].container_location == "B1"


def test_add_to_traction_qc_message(valid_sample):
    data = {
        "labwareType": "Plate12x8",
        "labwareUuid": "dd490ee5-fd1d-456d-99fd-eb9d3861e0f9".encode(),
        "barcode": "BARCODE001",
        "samples": [valid_sample],
    }
    instance = Labware(Input(data))
    assert instance.validate()

    traction_message = OutputTractionMessage()
    instance.add_to_message_property(traction_message)

    traction_qc_message = TractionQcMessage()
    instance.add_to_message_property(traction_qc_message)

    assert traction_qc_message._requests[0].sanger_sample_id == "cichlid_pacbio8196429"
    assert traction_qc_message._requests[0].container_barcode == "BARCODE001"
    assert traction_qc_message._requests[0].sheared_femto_fragment_size == "8"
    assert traction_qc_message._requests[0].post_spri_concentration == "9"
    assert traction_qc_message._requests[0].post_spri_volume == "10"
    assert traction_qc_message._requests[0].final_nano_drop_280 == "200"
    assert traction_qc_message._requests[0].final_nano_drop_230 == "200"
    assert traction_qc_message._requests[0].final_nano_drop == "150"
    assert traction_qc_message._requests[0].shearing_qc_comments == ""
