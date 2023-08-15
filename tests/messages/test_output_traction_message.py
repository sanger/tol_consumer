from tol_lab_share.messages.output_traction_message import OutputTractionMessage
from datetime import datetime
from tol_lab_share.constants import (
    OUTPUT_TRACTION_MESSAGE_CREATE_REQUEST_CONTAINER_TYPE_WELLS,
    OUTPUT_TRACTION_MESSAGE_CREATE_REQUEST_CONTAINER_TYPE_TUBES,
)
import requests_mock


def valid_traction_message():
    instance = OutputTractionMessage()
    instance.requests(0).container_barcode = "1"
    instance.requests(0).container_type = OUTPUT_TRACTION_MESSAGE_CREATE_REQUEST_CONTAINER_TYPE_WELLS
    instance.requests(0).library_type = "library"
    instance.requests(0).sample_name = "test1"
    instance.requests(0).study_uuid = "dd490ee5-fd1d-456d-99fd-eb9d3861e014"
    instance.requests(0).sample_uuid = "8860a6b4-82e2-451c-aba2-a3129c38c0fc"
    instance.requests(0).species = "test species"
    instance.requests(0).cost_code = "S1234"
    return instance


def test_output_traction_message_can_initialize():
    assert OutputTractionMessage() is not None


def test_output_traction_message_can_validate():
    instance = OutputTractionMessage()
    assert not instance.validate()

    instance = OutputTractionMessage()
    instance.requests(0).container_barcode = "1"
    instance.requests(0).container_type = "wells"
    instance.requests(0).library_type = "library"
    assert not instance.validate()

    assert valid_traction_message().validate()


def test_output_traction_message_can_generate_payload_for_plates():
    my_date = datetime.now()
    instance = OutputTractionMessage()
    instance.requests(0).container_barcode = "1"
    instance.requests(0).container_type = OUTPUT_TRACTION_MESSAGE_CREATE_REQUEST_CONTAINER_TYPE_WELLS
    instance.requests(1).container_location = "A1"
    instance.requests(0).library_type = "library"
    instance.requests(0).sample_name = "test1"
    instance.requests(0).study_uuid = "dd490ee5-fd1d-456d-99fd-eb9d3861e014"
    instance.requests(0).sample_uuid = "8860a6b4-82e2-451c-aba2-a3129c38c0fc"
    instance.requests(0).species = "test species"
    instance.requests(0).cost_code = "S1234"
    instance.requests(0).priority_level = None
    instance.requests(0).sanger_sample_id = "sample1"
    instance.requests(0).supplier_name = "supplier1"
    instance.requests(0).taxon_id = "9606"
    instance.requests(0).donor_id = "donor1"
    instance.requests(0).country_of_origin = "United Kingdom"
    instance.requests(0).accession_number = "AN1234"
    instance.requests(0).date_of_sample_collection = my_date

    instance.requests(1).container_barcode = "1"
    instance.requests(1).container_type = OUTPUT_TRACTION_MESSAGE_CREATE_REQUEST_CONTAINER_TYPE_WELLS
    instance.requests(1).container_location = "B1"
    instance.requests(1).library_type = "library"
    instance.requests(1).sample_name = "test1"
    instance.requests(1).study_uuid = "dd490ee5-fd1d-456d-99fd-eb9d3861e014"
    instance.requests(1).sample_uuid = "8860a6b4-82e2-451c-aba2-a3129c38c0fc"
    instance.requests(1).species = "test species"
    instance.requests(1).cost_code = "S4567"
    instance.requests(1).priority_level = None
    instance.requests(1).sanger_sample_id = "sample2"
    instance.requests(1).supplier_name = "supplier2"
    instance.requests(1).taxon_id = "9606"
    instance.requests(1).donor_id = "donor2"
    instance.requests(1).country_of_origin = "United Kingdom"
    instance.requests(1).accession_number = "AN1235"
    instance.requests(1).date_of_sample_collection = my_date

    assert instance.payload() == {
        "data": {
            "attributes": {
                "request_attributes": [
                    {
                        "container": {"barcode": "1", "position": None, "type": "wells"},
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
                            "supplier_name": "supplier1",
                            "taxon_id": "9606",
                            "donor_id": "donor1",
                            "country_of_origin": "United Kingdom",
                            "accession_number": "AN1234",
                            "date_of_sample_collection": my_date.strftime("%Y-%m-%d"),
                        },
                    },
                    {
                        "container": {"barcode": "1", "position": "B1", "type": "wells"},
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
                            "supplier_name": "supplier2",
                            "taxon_id": "9606",
                            "donor_id": "donor2",
                            "country_of_origin": "United Kingdom",
                            "accession_number": "AN1235",
                            "date_of_sample_collection": my_date.strftime("%Y-%m-%d"),
                        },
                    },
                ],
                "source": "tol-lab-share.tol",
            },
            "type": "receptions",
        }
    }


def test_output_traction_message_can_generate_payload_for_ont_library_types():
    my_date = datetime.now()
    instance = OutputTractionMessage()
    instance.requests(0).container_barcode = "1"
    instance.requests(0).container_type = OUTPUT_TRACTION_MESSAGE_CREATE_REQUEST_CONTAINER_TYPE_WELLS
    instance.requests(1).container_location = "A1"
    instance.requests(0).library_type = "ONT_mylib"
    instance.requests(0).sample_name = "test1"
    instance.requests(0).study_uuid = "dd490ee5-fd1d-456d-99fd-eb9d3861e014"
    instance.requests(0).sample_uuid = "8860a6b4-82e2-451c-aba2-a3129c38c0fc"
    instance.requests(0).species = "test species"
    instance.requests(0).cost_code = "S1234"
    instance.requests(0).priority_level = "Medium"
    instance.requests(0).sanger_sample_id = "sample1"
    instance.requests(0).supplier_name = "supplier1"
    instance.requests(0).taxon_id = "9606"
    instance.requests(0).donor_id = "donor1"
    instance.requests(0).country_of_origin = "United Kingdom"
    instance.requests(0).accession_number = "AN1234"
    instance.requests(0).date_of_sample_collection = my_date

    instance.requests(1).container_barcode = "1"
    instance.requests(1).container_type = OUTPUT_TRACTION_MESSAGE_CREATE_REQUEST_CONTAINER_TYPE_WELLS
    instance.requests(1).container_location = "B1"
    instance.requests(1).library_type = "ONT_mylib"
    instance.requests(1).sample_name = "test1"
    instance.requests(1).study_uuid = "dd490ee5-fd1d-456d-99fd-eb9d3861e014"
    instance.requests(1).sample_uuid = "8860a6b4-82e2-451c-aba2-a3129c38c0fc"
    instance.requests(1).species = "test species"
    instance.requests(1).cost_code = "S4567"
    instance.requests(1).priority_level = None
    instance.requests(1).sanger_sample_id = "sample2"
    instance.requests(1).supplier_name = "supplier2"
    instance.requests(1).taxon_id = "9606"
    instance.requests(1).donor_id = "donor2"
    instance.requests(1).country_of_origin = "United Kingdom"
    instance.requests(1).accession_number = "AN1235"
    instance.requests(1).date_of_sample_collection = my_date

    assert instance.payload() == {
        "data": {
            "attributes": {
                "request_attributes": [
                    {
                        "container": {"barcode": "1", "position": None, "type": "wells"},
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
                            "supplier_name": "supplier1",
                            "taxon_id": "9606",
                            "donor_id": "donor1",
                            "country_of_origin": "United Kingdom",
                            "accession_number": "AN1234",
                            "date_of_sample_collection": my_date.strftime("%Y-%m-%d"),
                        },
                    },
                    {
                        "container": {"barcode": "1", "position": "B1", "type": "wells"},
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
                            "supplier_name": "supplier2",
                            "taxon_id": "9606",
                            "donor_id": "donor2",
                            "country_of_origin": "United Kingdom",
                            "accession_number": "AN1235",
                            "date_of_sample_collection": my_date.strftime("%Y-%m-%d"),
                        },
                    },
                ],
                "source": "tol-lab-share.tol",
            },
            "type": "receptions",
        }
    }


def test_output_traction_message_can_generate_payload_for_tubes():
    my_date = datetime.now()
    instance = OutputTractionMessage()
    instance.requests(0).container_barcode = "1"
    instance.requests(0).container_type = OUTPUT_TRACTION_MESSAGE_CREATE_REQUEST_CONTAINER_TYPE_TUBES
    instance.requests(0).library_type = "library"
    instance.requests(0).sample_name = "test1"
    instance.requests(0).study_uuid = "dd490ee5-fd1d-456d-99fd-eb9d3861e014"
    instance.requests(0).sample_uuid = "8860a6b4-82e2-451c-aba2-a3129c38c0fc"
    instance.requests(0).species = "test species"
    instance.requests(0).cost_code = "S1234"
    instance.requests(0).priority_level = "High"
    instance.requests(0).sanger_sample_id = "sample1"
    instance.requests(0).supplier_name = "supplier1"
    instance.requests(0).taxon_id = "9606"
    instance.requests(0).donor_id = "donor1"
    instance.requests(0).country_of_origin = "United Kingdom"
    instance.requests(0).accession_number = "AN1234"
    instance.requests(0).date_of_sample_collection = my_date

    instance.requests(1).container_barcode = "1"
    instance.requests(1).container_type = OUTPUT_TRACTION_MESSAGE_CREATE_REQUEST_CONTAINER_TYPE_TUBES
    instance.requests(1).library_type = "library"
    instance.requests(1).sample_name = "test1"
    instance.requests(1).study_uuid = "dd490ee5-fd1d-456d-99fd-eb9d3861e014"
    instance.requests(1).sample_uuid = "8860a6b4-82e2-451c-aba2-a3129c38c0fc"
    instance.requests(1).species = "test species"
    instance.requests(1).cost_code = "S4567"
    instance.requests(1).priority_level = "Low"
    instance.requests(1).sanger_sample_id = "sample2"
    instance.requests(1).supplier_name = "supplier2"
    instance.requests(1).taxon_id = "9606"
    instance.requests(1).donor_id = "donor2"
    instance.requests(1).country_of_origin = "United Kingdom"
    instance.requests(1).accession_number = "AN1235"
    instance.requests(1).date_of_sample_collection = my_date

    assert instance.payload() == {
        "data": {
            "attributes": {
                "request_attributes": [
                    {
                        "container": {"barcode": "1", "type": "tubes"},
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
                            "supplier_name": "supplier1",
                            "taxon_id": "9606",
                            "donor_id": "donor1",
                            "country_of_origin": "United Kingdom",
                            "accession_number": "AN1234",
                            "date_of_sample_collection": my_date.strftime("%Y-%m-%d"),
                        },
                    },
                    {
                        "container": {"barcode": "1", "type": "tubes"},
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
                            "supplier_name": "supplier2",
                            "taxon_id": "9606",
                            "donor_id": "donor2",
                            "country_of_origin": "United Kingdom",
                            "accession_number": "AN1235",
                            "date_of_sample_collection": my_date.strftime("%Y-%m-%d"),
                        },
                    },
                ],
                "source": "tol-lab-share.tol",
            },
            "type": "receptions",
        }
    }


def test_output_traction_message_can_detect_errors_on_sent(config):
    vt = valid_traction_message()
    with requests_mock.Mocker() as m:
        m.post(config.TRACTION_URL, text="Error", status_code=422)
        vt.send(config.TRACTION_URL)
    assert not vt.validate()
    assert len(vt.errors) > 0


def test_output_traction_message_can_add_to_feedback_message_when_not_sent(valid_feedback_message):
    vt = valid_traction_message()
    assert vt.validate()
    feedback = valid_feedback_message
    vt.add_to_feedback_message(feedback)
    assert len(feedback.errors) == 0
    # When message not sent
    assert not feedback.operation_was_error_free


def test_output_traction_message_can_add_to_feedback_message_when_sent(
    config, traction_success_creation_response, valid_feedback_message
):
    vt = valid_traction_message()
    feedback = valid_feedback_message
    # When message sent
    with requests_mock.Mocker() as m:
        m.post(config.TRACTION_URL, json=traction_success_creation_response, status_code=201)
        vt.send(config.TRACTION_URL)
    vt.add_to_feedback_message(feedback)
    assert len(feedback.errors) == 0
    assert feedback.operation_was_error_free


def test_output_traction_message_can_add_to_feedback_message_when_errors(valid_feedback_message):
    instance = OutputTractionMessage()
    instance.requests(0).container_barcode = "1"
    instance.requests(0).container_type = OUTPUT_TRACTION_MESSAGE_CREATE_REQUEST_CONTAINER_TYPE_TUBES
    assert not instance.validate()
    feedback = valid_feedback_message
    instance.add_to_feedback_message(feedback)
    assert len(feedback.errors) > 0
    assert not feedback.operation_was_error_free
