from tol_lab_share.messages.properties.complex.labware import Labware
from tol_lab_share.messages.properties.complex.location import Location
from tol_lab_share.messages.properties.simple.value import Value
from tol_lab_share.messages.traction import TractionReceptionMessage, TractionQcMessage


class TestLabware:
    def test_validators_when_data_is_valid(self):
        labware = {
            "labwareType": "Plate12x8",
            "labwareUuid": "dd490ee5-fd1d-456d-99fd-eb9d3861e0f9".encode(),
            "barcode": "BARCODE001",
            "samples": [],
        }

        instance = Labware(Value(labware))
        assert instance.validate() is True
        assert instance.errors == []

    def test_validators_when_barcode_is_invalid(self):
        labware = {
            "labwareType": "Plate12x9",
            "labwareUuid": "dd490ee5-fd1d-456d-99fd-eb9d3861e0f9",
            "barcode": 1234,
            "samples": [],
        }

        instance = Labware(Value(labware))
        assert instance.validate() is False
        assert len(instance.errors) > 0

    def test_validators_when_barcode_is_missing(self):
        labware = {
            "labwareType": "Plate12x8",
            "labwareUuid": "dd490ee5-fd1d-456d-99fd-eb9d3861e0f9".encode(),
            "samples": [],
        }
        instance = Labware(Value(labware))
        assert instance.validate() is False
        assert len(instance.errors) > 0

    def test_count_of_total_samples(self, valid_sample):
        labware = {
            "labwareType": "Plate12x8",
            "labwareUuid": "dd490ee5-fd1d-456d-99fd-eb9d3861e0f9".encode(),
            "barcode": "1234",
            "samples": [],
        }

        instance = Labware(Value(labware))
        assert instance.validate()
        assert instance.errors == []
        assert instance.count_of_total_samples() == 0

        labware2 = {
            "labwareType": "Plate12x8",
            "labwareUuid": "dd490ee5-fd1d-456d-99fd-eb9d3861e0f9".encode(),
            "barcode": "1234",
            "samples": [valid_sample, valid_sample],
        }

        instance = Labware(Value(labware2))
        assert instance.validate()
        assert instance.errors == []
        assert instance.count_of_total_samples() == 2

    def test_count_of_valid_samples(self, valid_sample, invalid_sample):
        labware = {
            "labwareType": "Plate12x8",
            "labwareUuid": b"dd490ee5-fd1d-456d-99fd-eb9d3861e0f9",
            "barcode": "1234",
            "samples": [],
        }

        instance = Labware(Value(labware))
        instance.validate()
        assert instance.errors == []
        assert instance.count_of_valid_samples() == 0

        labware2 = {
            "labwareType": "Plate12x8",
            "labwareUuid": b"dd490ee5-fd1d-456d-99fd-eb9d3861e0f9",
            "barcode": "1234",
            "samples": [valid_sample, valid_sample],
        }

        instance = Labware(Value(labware2))
        instance.validate()
        assert instance.errors == []
        assert instance.count_of_valid_samples() == 2

        labware2 = {
            "labwareType": "Plate12x8",
            "labwareUuid": b"dd490ee5-fd1d-456d-99fd-eb9d3861e0f9",
            "barcode": "1234",
            "samples": [invalid_sample, valid_sample],
        }

        instance = Labware(Value(labware2))
        instance.validate()
        assert instance.count_of_valid_samples() == 1

    def test_add_to_traction_reception_message_with_plate(self, valid_sample):
        data = {
            "labwareType": "Plate12x8",
            "labwareUuid": "dd490ee5-fd1d-456d-99fd-eb9d3861e0f9".encode(),
            "barcode": "BARCODE001",
            "samples": [valid_sample],
        }
        instance = Labware(Value(data))
        assert instance.validate()

        traction_message = TractionReceptionMessage()
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

    def test_add_to_traction_reception_message_with_tube(self, valid_sample):
        data = {
            "labwareType": "Tube",
            "labwareUuid": "dd490ee5-fd1d-456d-99fd-eb9d3861e0f9".encode(),
            "barcode": "BARCODE001",
            "samples": [valid_sample],
        }
        instance = Labware(Value(data))

        traction_message = TractionReceptionMessage()
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

    def test_add_to_traction_reception_message_uses_unpadded_location(self, valid_sample):
        data = {
            "labwareType": "Plate12x8",
            "labwareUuid": "dd490ee5-fd1d-456d-99fd-eb9d3861e0f9".encode(),
            "barcode": "BARCODE001",
            "samples": [valid_sample],
        }
        instance = Labware(Value(data))
        instance.properties("samples")[0].add_property("location", Location(Value("B01")))
        traction_message = TractionReceptionMessage()
        instance.add_to_message_property(traction_message)
        assert traction_message._requests[0].container_location == "B1"

    def test_add_to_traction_qc_message(self, valid_sample):
        data = {
            "labwareType": "Plate12x8",
            "labwareUuid": "dd490ee5-fd1d-456d-99fd-eb9d3861e0f9".encode(),
            "barcode": "BARCODE001",
            "samples": [valid_sample],
        }
        instance = Labware(Value(data))
        assert instance.validate()

        traction_message = TractionReceptionMessage()
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
