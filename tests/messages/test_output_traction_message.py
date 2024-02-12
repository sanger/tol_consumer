from tol_lab_share.messages.output_traction_message import OutputTractionMessage
from datetime import datetime
import requests_mock


def valid_traction_message():
    instance = OutputTractionMessage()
    request = instance.create_request()
    request.container_barcode = "1"
    request.container_type = "wells"
    request.library_type = "library"
    request.sample_name = "test1"
    request.study_uuid = "dd490ee5-fd1d-456d-99fd-eb9d3861e014"
    request.sample_uuid = "8860a6b4-82e2-451c-aba2-a3129c38c0fc"
    request.species = "test species"
    request.cost_code = "S1234"

    return instance


def test_output_traction_message_can_initialize():
    assert OutputTractionMessage() is not None


def test_output_traction_message_can_validate():
    instance = OutputTractionMessage()
    assert not instance.validate()

    instance = OutputTractionMessage()
    request = instance.create_request()
    request.container_barcode = "1"
    request.container_type = "wells"
    request.library_type = "library"
    assert not instance.validate()

    assert valid_traction_message().validate()


def test_output_traction_message_can_generate_payload_for_plates():
    my_date = datetime.now()
    instance = OutputTractionMessage()

    request = instance.create_request()
    request.container_barcode = "1"
    request.container_type = "wells"
    request.container_location = "A1"
    request.library_type = "library"
    request.sample_name = "test1"
    request.study_uuid = "dd490ee5-fd1d-456d-99fd-eb9d3861e014"
    request.sample_uuid = "8860a6b4-82e2-451c-aba2-a3129c38c0fc"
    request.species = "test species"
    request.public_name = "Public1"
    request.cost_code = "S1234"
    request.priority_level = None
    request.sanger_sample_id = "sample1"
    request.supplier_name = "supplier1"
    request.taxon_id = "9606"
    request.donor_id = "donor1"
    request.country_of_origin = "United Kingdom"
    request.accession_number = "AN1234"
    request.date_of_sample_collection = my_date

    request = instance.create_request()
    request.container_barcode = "1"
    request.container_type = "wells"
    request.container_location = "B1"
    request.library_type = "library"
    request.sample_name = "test1"
    request.study_uuid = "dd490ee5-fd1d-456d-99fd-eb9d3861e014"
    request.sample_uuid = "8860a6b4-82e2-451c-aba2-a3129c38c0fc"
    request.species = "test species"
    request.public_name = "Public2"
    request.cost_code = "S4567"
    request.priority_level = None
    request.sanger_sample_id = "sample2"
    request.supplier_name = "supplier2"
    request.taxon_id = "9606"
    request.donor_id = "donor2"
    request.country_of_origin = "United Kingdom"
    request.accession_number = "AN1235"
    request.date_of_sample_collection = my_date

    assert instance.payload() == {
        "data": {
            "type": "receptions",
            "attributes": {
                "source": "tol-lab-share.tol",
                "plates_attributes": [
                    {
                        "barcode": "1",
                        "type": "plates",
                        "wells_attributes": [
                            {
                                "position": "A1",
                                "request": {
                                    "external_study_id": "dd490ee5-fd1d-456d-99fd-eb9d3861e014",
                                    "library_type": "library",
                                    "cost_code": "S1234",
                                },
                                "sample": {
                                    "external_id": "8860a6b4-82e2-451c-aba2-a3129c38c0fc",
                                    "name": "test1",
                                    "species": "test " "species",
                                    "priority_level": None,
                                    "sanger_sample_id": "sample1",
                                    "public_name": "Public1",
                                    "supplier_name": "supplier1",
                                    "taxon_id": "9606",
                                    "donor_id": "donor1",
                                    "country_of_origin": "United Kingdom",
                                    "accession_number": "AN1234",
                                    "date_of_sample_collection": my_date.strftime("%Y-%m-%d"),
                                },
                            },
                            {
                                "position": "B1",
                                "request": {
                                    "external_study_id": "dd490ee5-fd1d-456d-99fd-eb9d3861e014",
                                    "library_type": "library",
                                    "cost_code": "S4567",
                                },
                                "sample": {
                                    "external_id": "8860a6b4-82e2-451c-aba2-a3129c38c0fc",
                                    "name": "test1",
                                    "species": "test " "species",
                                    "priority_level": None,
                                    "sanger_sample_id": "sample2",
                                    "public_name": "Public2",
                                    "supplier_name": "supplier2",
                                    "taxon_id": "9606",
                                    "donor_id": "donor2",
                                    "country_of_origin": "United Kingdom",
                                    "accession_number": "AN1235",
                                    "date_of_sample_collection": my_date.strftime("%Y-%m-%d"),
                                },
                            },
                        ],
                    },
                ],
                "tubes_attributes": [],
            },
        }
    }


def test_output_traction_message_can_generate_payload_for_ont_library_types():
    my_date = datetime.now()
    instance = OutputTractionMessage()

    request = instance.create_request()
    request.container_barcode = "1"
    request.container_type = "wells"
    request.container_location = "A1"
    request.library_type = "ONT_mylib"
    request.sample_name = "test1"
    request.study_uuid = "dd490ee5-fd1d-456d-99fd-eb9d3861e014"
    request.sample_uuid = "8860a6b4-82e2-451c-aba2-a3129c38c0fc"
    request.species = "test species"
    request.public_name = "Public1"
    request.cost_code = "S1234"
    request.priority_level = "Medium"
    request.sanger_sample_id = "sample1"
    request.supplier_name = "supplier1"
    request.taxon_id = "9606"
    request.donor_id = "donor1"
    request.country_of_origin = "United Kingdom"
    request.accession_number = "AN1234"
    request.date_of_sample_collection = my_date

    request = instance.create_request()
    request.container_barcode = "1"
    request.container_type = "wells"
    request.container_location = "B1"
    request.library_type = "ONT_mylib"
    request.sample_name = "test1"
    request.study_uuid = "dd490ee5-fd1d-456d-99fd-eb9d3861e014"
    request.sample_uuid = "8860a6b4-82e2-451c-aba2-a3129c38c0fc"
    request.species = "test species"
    request.public_name = "Public2"
    request.cost_code = "S4567"
    request.priority_level = None
    request.sanger_sample_id = "sample2"
    request.supplier_name = "supplier2"
    request.taxon_id = "9606"
    request.donor_id = "donor2"
    request.country_of_origin = "United Kingdom"
    request.accession_number = "AN1235"
    request.date_of_sample_collection = my_date

    assert instance.payload() == {
        "data": {
            "type": "receptions",
            "attributes": {
                "source": "tol-lab-share.tol",
                "plates_attributes": [
                    {
                        "barcode": "1",
                        "type": "plates",
                        "wells_attributes": [
                            {
                                "position": "A1",
                                "request": {
                                    "external_study_id": "dd490ee5-fd1d-456d-99fd-eb9d3861e014",
                                    "library_type": "ONT_mylib",
                                    "cost_code": "S1234",
                                    "data_type": "basecalls",
                                },
                                "sample": {
                                    "external_id": "8860a6b4-82e2-451c-aba2-a3129c38c0fc",
                                    "name": "test1",
                                    "species": "test " "species",
                                    "priority_level": "Medium",
                                    "sanger_sample_id": "sample1",
                                    "public_name": "Public1",
                                    "supplier_name": "supplier1",
                                    "taxon_id": "9606",
                                    "donor_id": "donor1",
                                    "country_of_origin": "United Kingdom",
                                    "accession_number": "AN1234",
                                    "date_of_sample_collection": my_date.strftime("%Y-%m-%d"),
                                },
                            },
                            {
                                "position": "B1",
                                "request": {
                                    "external_study_id": "dd490ee5-fd1d-456d-99fd-eb9d3861e014",
                                    "library_type": "ONT_mylib",
                                    "cost_code": "S4567",
                                    "data_type": "basecalls",
                                },
                                "sample": {
                                    "external_id": "8860a6b4-82e2-451c-aba2-a3129c38c0fc",
                                    "name": "test1",
                                    "species": "test " "species",
                                    "priority_level": None,
                                    "sanger_sample_id": "sample2",
                                    "public_name": "Public2",
                                    "supplier_name": "supplier2",
                                    "taxon_id": "9606",
                                    "donor_id": "donor2",
                                    "country_of_origin": "United Kingdom",
                                    "accession_number": "AN1235",
                                    "date_of_sample_collection": my_date.strftime("%Y-%m-%d"),
                                },
                            },
                        ],
                    },
                ],
                "tubes_attributes": [],
            },
        }
    }


def test_output_traction_message_can_generate_payload_for_tubes():
    my_date = datetime.now()
    instance = OutputTractionMessage()

    request = instance.create_request()
    request.container_barcode = "1"
    request.container_type = "tubes"
    request.library_type = "library"
    request.sample_name = "test1"
    request.study_uuid = "dd490ee5-fd1d-456d-99fd-eb9d3861e014"
    request.sample_uuid = "8860a6b4-82e2-451c-aba2-a3129c38c0fc"
    request.species = "test species"
    request.public_name = "Public1"
    request.cost_code = "S1234"
    request.priority_level = "High"
    request.sanger_sample_id = "sample1"
    request.supplier_name = "supplier1"
    request.taxon_id = "9606"
    request.donor_id = "donor1"
    request.country_of_origin = "United Kingdom"
    request.accession_number = "AN1234"
    request.date_of_sample_collection = my_date

    request = instance.create_request()
    request.container_barcode = "1"
    request.container_type = "tubes"
    request.library_type = "library"
    request.sample_name = "test1"
    request.study_uuid = "dd490ee5-fd1d-456d-99fd-eb9d3861e014"
    request.sample_uuid = "8860a6b4-82e2-451c-aba2-a3129c38c0fc"
    request.species = "test species"
    request.public_name = "Public2"
    request.cost_code = "S4567"
    request.priority_level = "Low"
    request.sanger_sample_id = "sample2"
    request.supplier_name = "supplier2"
    request.taxon_id = "9606"
    request.donor_id = "donor2"
    request.country_of_origin = "United Kingdom"
    request.accession_number = "AN1235"
    request.date_of_sample_collection = my_date

    assert instance.payload() == {
        "data": {
            "type": "receptions",
            "attributes": {
                "source": "tol-lab-share.tol",
                "plates_attributes": [],
                "tubes_attributes": [
                    {
                        "barcode": "1",
                        "type": "tubes",
                        "request": {
                            "external_study_id": "dd490ee5-fd1d-456d-99fd-eb9d3861e014",
                            "library_type": "library",
                            "cost_code": "S1234",
                        },
                        "sample": {
                            "external_id": "8860a6b4-82e2-451c-aba2-a3129c38c0fc",
                            "name": "test1",
                            "species": "test " "species",
                            "priority_level": "High",
                            "sanger_sample_id": "sample1",
                            "public_name": "Public1",
                            "supplier_name": "supplier1",
                            "taxon_id": "9606",
                            "donor_id": "donor1",
                            "country_of_origin": "United Kingdom",
                            "accession_number": "AN1234",
                            "date_of_sample_collection": my_date.strftime("%Y-%m-%d"),
                        },
                    },
                    {
                        "barcode": "1",
                        "type": "tubes",
                        "request": {
                            "external_study_id": "dd490ee5-fd1d-456d-99fd-eb9d3861e014",
                            "library_type": "library",
                            "cost_code": "S4567",
                        },
                        "sample": {
                            "external_id": "8860a6b4-82e2-451c-aba2-a3129c38c0fc",
                            "name": "test1",
                            "species": "test " "species",
                            "priority_level": "Low",
                            "sanger_sample_id": "sample2",
                            "public_name": "Public2",
                            "supplier_name": "supplier2",
                            "taxon_id": "9606",
                            "donor_id": "donor2",
                            "country_of_origin": "United Kingdom",
                            "accession_number": "AN1235",
                            "date_of_sample_collection": my_date.strftime("%Y-%m-%d"),
                        },
                    },
                ],
            },
        }
    }


def test_output_traction_message_can_detect_errors_on_sent(config):
    vt = valid_traction_message()

    with requests_mock.Mocker() as m:
        m.post(config.TRACTION_URL, text="Error", status_code=422)
        vt.send(config.TRACTION_URL)

    assert not vt.validate()
    assert len(vt.errors) > 0


def test_output_traction_message_can_add_to_message_property_when_not_sent(valid_feedback_message):
    vt = valid_traction_message()

    assert vt.validate()

    feedback = valid_feedback_message
    vt.add_to_message_property(feedback)

    assert len(feedback.errors) == 0
    assert not feedback.operation_was_error_free


def test_output_traction_message_can_add_to_message_property_when_sent(
    config, traction_success_creation_response, valid_feedback_message
):
    vt = valid_traction_message()
    feedback = valid_feedback_message

    with requests_mock.Mocker() as m:
        m.post(config.TRACTION_URL, json=traction_success_creation_response, status_code=201)
        vt.send(config.TRACTION_URL)

    vt.add_to_message_property(feedback)

    assert len(feedback.errors) == 0
    assert feedback.operation_was_error_free


def test_output_traction_message_can_add_to_message_property_when_errors(valid_feedback_message):
    instance = OutputTractionMessage()

    request = instance.create_request()
    request.container_barcode = "1"
    request.container_type = "tubes"

    assert not instance.validate()

    feedback = valid_feedback_message
    instance.add_to_message_property(feedback)

    assert len(feedback.errors) > 0
    assert not feedback.operation_was_error_free
