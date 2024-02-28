from tol_lab_share.traction.output_traction_message import OutputTractionMessage
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
    my_date = datetime.utcnow()
    instance = OutputTractionMessage()

    request = instance.create_request()
    request.accession_number = "AN1234"
    request.container_barcode = "1"
    request.container_location = "A1"
    request.container_type = "wells"
    request.cost_code = "S1234"
    request.country_of_origin = "United Kingdom"
    request.date_of_sample_collection = my_date
    request.donor_id = "donor1"
    request.genome_size = "123,456,789"
    request.library_type = "library"
    request.priority_level = None
    request.public_name = "Public1"
    request.sample_name = "test1"
    request.sample_uuid = "8860a6b4-82e2-451c-aba2-a3129c38c0fc"
    request.sanger_sample_id = "sample1"
    request.species = "test species"
    request.study_uuid = "dd490ee5-fd1d-456d-99fd-eb9d3861e014"
    request.supplier_name = "supplier1"
    request.taxon_id = "9606"

    request = instance.create_request()
    request.accession_number = "AN1235"
    request.container_barcode = "1"
    request.container_location = "B1"
    request.container_type = "wells"
    request.cost_code = "S4567"
    request.country_of_origin = "United Kingdom"
    request.date_of_sample_collection = my_date
    request.donor_id = "donor2"
    request.genome_size = None
    request.library_type = "library"
    request.priority_level = None
    request.public_name = "Public2"
    request.sample_name = "test1"
    request.sample_uuid = "8860a6b4-82e2-451c-aba2-a3129c38c0fc"
    request.sanger_sample_id = "sample2"
    request.species = "test species"
    request.study_uuid = "dd490ee5-fd1d-456d-99fd-eb9d3861e014"
    request.supplier_name = "supplier2"
    request.taxon_id = "9606"

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
                                    "cost_code": "S1234",
                                    "estimate_of_gb_required": "123,456,789",
                                    "external_study_id": "dd490ee5-fd1d-456d-99fd-eb9d3861e014",
                                    "library_type": "library",
                                },
                                "sample": {
                                    "accession_number": "AN1234",
                                    "country_of_origin": "United Kingdom",
                                    "date_of_sample_collection": my_date.strftime("%Y-%m-%d"),
                                    "donor_id": "donor1",
                                    "external_id": "8860a6b4-82e2-451c-aba2-a3129c38c0fc",
                                    "name": "test1",
                                    "priority_level": None,
                                    "public_name": "Public1",
                                    "sanger_sample_id": "sample1",
                                    "species": "test " "species",
                                    "supplier_name": "supplier1",
                                    "taxon_id": "9606",
                                },
                            },
                            {
                                "position": "B1",
                                "request": {
                                    "cost_code": "S4567",
                                    "estimate_of_gb_required": None,
                                    "external_study_id": "dd490ee5-fd1d-456d-99fd-eb9d3861e014",
                                    "library_type": "library",
                                },
                                "sample": {
                                    "accession_number": "AN1235",
                                    "country_of_origin": "United Kingdom",
                                    "date_of_sample_collection": my_date.strftime("%Y-%m-%d"),
                                    "donor_id": "donor2",
                                    "external_id": "8860a6b4-82e2-451c-aba2-a3129c38c0fc",
                                    "name": "test1",
                                    "priority_level": None,
                                    "public_name": "Public2",
                                    "sanger_sample_id": "sample2",
                                    "species": "test " "species",
                                    "supplier_name": "supplier2",
                                    "taxon_id": "9606",
                                },
                            },
                        ],
                    },
                ],
                "tubes_attributes": [],
            },
        }
    }


def test_output_traction_message_can_generate_payload_for_multiple_plates():
    my_date = datetime.utcnow()
    instance = OutputTractionMessage()

    # Mix the order of the requests to ensure the grouping for plates works.
    # Well order is still maintained since the payload keeps the order of the requests.

    # First plate, first well (A1).
    request = instance.create_request()
    request.accession_number = "AN1234"
    request.container_barcode = "123"
    request.container_location = "A1"
    request.container_type = "wells"
    request.cost_code = "S1234"
    request.country_of_origin = "United Kingdom"
    request.date_of_sample_collection = my_date
    request.donor_id = "donor1"
    request.genome_size = "123,456,789"
    request.library_type = "library"
    request.priority_level = None
    request.public_name = "Public1"
    request.sample_name = "test1"
    request.sample_uuid = "8860a6b4-1234-451c-aba2-a3129c38c0fc"
    request.sanger_sample_id = "sample1"
    request.species = "test species"
    request.study_uuid = "dd490ee5-fd1d-456d-99fd-eb9d3861e014"
    request.supplier_name = "supplier1"
    request.taxon_id = "9606"

    # Second plate, first well (B1).
    request = instance.create_request()
    request.accession_number = "AN1236"
    request.container_barcode = "456"
    request.container_location = "B1"
    request.container_type = "wells"
    request.cost_code = "S1234"
    request.country_of_origin = "United Kingdom"
    request.date_of_sample_collection = my_date
    request.donor_id = "donor3"
    request.genome_size = None
    request.library_type = "library"
    request.priority_level = None
    request.public_name = "Public3"
    request.sample_name = "test3"
    request.sample_uuid = "8860a6b4-1236-451c-aba2-a3129c38c0fc"
    request.sanger_sample_id = "sample3"
    request.species = "test species"
    request.study_uuid = "dd490ee5-fd1d-456d-99fd-eb9d3861e014"
    request.supplier_name = "supplier1"
    request.taxon_id = "9606"

    # First plate, second well (B1).
    request = instance.create_request()
    request.accession_number = "AN1235"
    request.container_barcode = "123"
    request.container_location = "B1"
    request.container_type = "wells"
    request.cost_code = "S4567"
    request.country_of_origin = "United Kingdom"
    request.date_of_sample_collection = my_date
    request.donor_id = "donor2"
    request.genome_size = None
    request.library_type = "library"
    request.priority_level = None
    request.public_name = "Public2"
    request.sample_name = "test2"
    request.sample_uuid = "8860a6b4-1235-451c-aba2-a3129c38c0fc"
    request.sanger_sample_id = "sample2"
    request.species = "test species"
    request.study_uuid = "dd490ee5-fd1d-456d-99fd-eb9d3861e014"
    request.supplier_name = "supplier2"
    request.taxon_id = "9606"

    # Second plate, second well (C1).
    request = instance.create_request()
    request.accession_number = "AN1237"
    request.container_barcode = "456"
    request.container_location = "C1"
    request.container_type = "wells"
    request.cost_code = "S4567"
    request.country_of_origin = "United Kingdom"
    request.date_of_sample_collection = my_date
    request.donor_id = "donor4"
    request.genome_size = "987,654,321"
    request.library_type = "library"
    request.priority_level = None
    request.public_name = "Public4"
    request.sample_name = "test4"
    request.sample_uuid = "8860a6b4-1237-451c-aba2-a3129c38c0fc"
    request.sanger_sample_id = "sample4"
    request.species = "test species"
    request.study_uuid = "dd490ee5-fd1d-456d-99fd-eb9d3861e014"
    request.supplier_name = "supplier2"
    request.taxon_id = "9606"

    assert instance.payload() == {
        "data": {
            "type": "receptions",
            "attributes": {
                "source": "tol-lab-share.tol",
                "plates_attributes": [
                    {
                        "barcode": "123",
                        "type": "plates",
                        "wells_attributes": [
                            {
                                "position": "A1",
                                "request": {
                                    "cost_code": "S1234",
                                    "estimate_of_gb_required": "123,456,789",
                                    "external_study_id": "dd490ee5-fd1d-456d-99fd-eb9d3861e014",
                                    "library_type": "library",
                                },
                                "sample": {
                                    "accession_number": "AN1234",
                                    "country_of_origin": "United Kingdom",
                                    "date_of_sample_collection": my_date.strftime("%Y-%m-%d"),
                                    "donor_id": "donor1",
                                    "external_id": "8860a6b4-1234-451c-aba2-a3129c38c0fc",
                                    "name": "test1",
                                    "priority_level": None,
                                    "public_name": "Public1",
                                    "sanger_sample_id": "sample1",
                                    "species": "test " "species",
                                    "supplier_name": "supplier1",
                                    "taxon_id": "9606",
                                },
                            },
                            {
                                "position": "B1",
                                "request": {
                                    "cost_code": "S4567",
                                    "estimate_of_gb_required": None,
                                    "external_study_id": "dd490ee5-fd1d-456d-99fd-eb9d3861e014",
                                    "library_type": "library",
                                },
                                "sample": {
                                    "accession_number": "AN1235",
                                    "country_of_origin": "United Kingdom",
                                    "date_of_sample_collection": my_date.strftime("%Y-%m-%d"),
                                    "donor_id": "donor2",
                                    "external_id": "8860a6b4-1235-451c-aba2-a3129c38c0fc",
                                    "name": "test2",
                                    "priority_level": None,
                                    "public_name": "Public2",
                                    "sanger_sample_id": "sample2",
                                    "species": "test " "species",
                                    "supplier_name": "supplier2",
                                    "taxon_id": "9606",
                                },
                            },
                        ],
                    },
                    {
                        "barcode": "456",
                        "type": "plates",
                        "wells_attributes": [
                            {
                                "position": "B1",
                                "request": {
                                    "cost_code": "S1234",
                                    "estimate_of_gb_required": None,
                                    "external_study_id": "dd490ee5-fd1d-456d-99fd-eb9d3861e014",
                                    "library_type": "library",
                                },
                                "sample": {
                                    "accession_number": "AN1236",
                                    "country_of_origin": "United Kingdom",
                                    "date_of_sample_collection": my_date.strftime("%Y-%m-%d"),
                                    "donor_id": "donor3",
                                    "external_id": "8860a6b4-1236-451c-aba2-a3129c38c0fc",
                                    "name": "test3",
                                    "priority_level": None,
                                    "public_name": "Public3",
                                    "sanger_sample_id": "sample3",
                                    "species": "test " "species",
                                    "supplier_name": "supplier1",
                                    "taxon_id": "9606",
                                },
                            },
                            {
                                "position": "C1",
                                "request": {
                                    "cost_code": "S4567",
                                    "estimate_of_gb_required": "987,654,321",
                                    "external_study_id": "dd490ee5-fd1d-456d-99fd-eb9d3861e014",
                                    "library_type": "library",
                                },
                                "sample": {
                                    "accession_number": "AN1237",
                                    "country_of_origin": "United Kingdom",
                                    "date_of_sample_collection": my_date.strftime("%Y-%m-%d"),
                                    "donor_id": "donor4",
                                    "external_id": "8860a6b4-1237-451c-aba2-a3129c38c0fc",
                                    "name": "test4",
                                    "priority_level": None,
                                    "public_name": "Public4",
                                    "sanger_sample_id": "sample4",
                                    "species": "test " "species",
                                    "supplier_name": "supplier2",
                                    "taxon_id": "9606",
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
    my_date = datetime.utcnow()
    instance = OutputTractionMessage()

    request = instance.create_request()
    request.accession_number = "AN1234"
    request.container_barcode = "1"
    request.container_location = "A1"
    request.container_type = "wells"
    request.cost_code = "S1234"
    request.country_of_origin = "United Kingdom"
    request.date_of_sample_collection = my_date
    request.donor_id = "donor1"
    request.genome_size = None
    request.library_type = "ONT_mylib"
    request.priority_level = "Medium"
    request.public_name = "Public1"
    request.sample_name = "test1"
    request.sample_uuid = "8860a6b4-82e2-451c-aba2-a3129c38c0fc"
    request.sanger_sample_id = "sample1"
    request.species = "test species"
    request.study_uuid = "dd490ee5-fd1d-456d-99fd-eb9d3861e014"
    request.supplier_name = "supplier1"
    request.taxon_id = "9606"

    request = instance.create_request()
    request.accession_number = "AN1235"
    request.container_barcode = "1"
    request.container_location = "B1"
    request.container_type = "wells"
    request.cost_code = "S4567"
    request.country_of_origin = "United Kingdom"
    request.date_of_sample_collection = my_date
    request.donor_id = "donor2"
    request.genome_size = None
    request.library_type = "ONT_mylib"
    request.priority_level = None
    request.public_name = "Public2"
    request.sample_name = "test1"
    request.sample_uuid = "8860a6b4-82e2-451c-aba2-a3129c38c0fc"
    request.sanger_sample_id = "sample2"
    request.species = "test species"
    request.study_uuid = "dd490ee5-fd1d-456d-99fd-eb9d3861e014"
    request.supplier_name = "supplier2"
    request.taxon_id = "9606"

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
                                    "cost_code": "S1234",
                                    "data_type": "basecalls",
                                    "estimate_of_gb_required": None,
                                    "external_study_id": "dd490ee5-fd1d-456d-99fd-eb9d3861e014",
                                    "library_type": "ONT_mylib",
                                },
                                "sample": {
                                    "accession_number": "AN1234",
                                    "country_of_origin": "United Kingdom",
                                    "date_of_sample_collection": my_date.strftime("%Y-%m-%d"),
                                    "donor_id": "donor1",
                                    "external_id": "8860a6b4-82e2-451c-aba2-a3129c38c0fc",
                                    "name": "test1",
                                    "priority_level": "Medium",
                                    "public_name": "Public1",
                                    "sanger_sample_id": "sample1",
                                    "species": "test " "species",
                                    "supplier_name": "supplier1",
                                    "taxon_id": "9606",
                                },
                            },
                            {
                                "position": "B1",
                                "request": {
                                    "cost_code": "S4567",
                                    "data_type": "basecalls",
                                    "estimate_of_gb_required": None,
                                    "external_study_id": "dd490ee5-fd1d-456d-99fd-eb9d3861e014",
                                    "library_type": "ONT_mylib",
                                },
                                "sample": {
                                    "accession_number": "AN1235",
                                    "country_of_origin": "United Kingdom",
                                    "date_of_sample_collection": my_date.strftime("%Y-%m-%d"),
                                    "donor_id": "donor2",
                                    "external_id": "8860a6b4-82e2-451c-aba2-a3129c38c0fc",
                                    "name": "test1",
                                    "priority_level": None,
                                    "public_name": "Public2",
                                    "sanger_sample_id": "sample2",
                                    "species": "test " "species",
                                    "supplier_name": "supplier2",
                                    "taxon_id": "9606",
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
    my_date = datetime.utcnow()
    instance = OutputTractionMessage()

    request = instance.create_request()
    request.accession_number = "AN1234"
    request.container_barcode = "1"
    request.container_type = "tubes"
    request.cost_code = "S1234"
    request.country_of_origin = "United Kingdom"
    request.date_of_sample_collection = my_date
    request.donor_id = "donor1"
    request.genome_size = "123,456,789"
    request.library_type = "library"
    request.priority_level = "High"
    request.public_name = "Public1"
    request.sample_name = "test1"
    request.sample_uuid = "8860a6b4-82e2-451c-aba2-a3129c38c0fc"
    request.sanger_sample_id = "sample1"
    request.species = "test species"
    request.study_uuid = "dd490ee5-fd1d-456d-99fd-eb9d3861e014"
    request.supplier_name = "supplier1"
    request.taxon_id = "9606"

    request = instance.create_request()
    request.accession_number = "AN1235"
    request.container_barcode = "1"
    request.container_type = "tubes"
    request.cost_code = "S4567"
    request.country_of_origin = "United Kingdom"
    request.date_of_sample_collection = my_date
    request.donor_id = "donor2"
    request.genome_size = "987,654,321"
    request.library_type = "library"
    request.priority_level = "Low"
    request.public_name = "Public2"
    request.sample_name = "test1"
    request.sample_uuid = "8860a6b4-82e2-451c-aba2-a3129c38c0fc"
    request.sanger_sample_id = "sample2"
    request.species = "test species"
    request.study_uuid = "dd490ee5-fd1d-456d-99fd-eb9d3861e014"
    request.supplier_name = "supplier2"
    request.taxon_id = "9606"

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
                            "cost_code": "S1234",
                            "estimate_of_gb_required": "123,456,789",
                            "external_study_id": "dd490ee5-fd1d-456d-99fd-eb9d3861e014",
                            "library_type": "library",
                        },
                        "sample": {
                            "accession_number": "AN1234",
                            "country_of_origin": "United Kingdom",
                            "date_of_sample_collection": my_date.strftime("%Y-%m-%d"),
                            "donor_id": "donor1",
                            "external_id": "8860a6b4-82e2-451c-aba2-a3129c38c0fc",
                            "name": "test1",
                            "priority_level": "High",
                            "public_name": "Public1",
                            "sanger_sample_id": "sample1",
                            "species": "test " "species",
                            "supplier_name": "supplier1",
                            "taxon_id": "9606",
                        },
                    },
                    {
                        "barcode": "1",
                        "type": "tubes",
                        "request": {
                            "cost_code": "S4567",
                            "estimate_of_gb_required": "987,654,321",
                            "external_study_id": "dd490ee5-fd1d-456d-99fd-eb9d3861e014",
                            "library_type": "library",
                        },
                        "sample": {
                            "accession_number": "AN1235",
                            "country_of_origin": "United Kingdom",
                            "date_of_sample_collection": my_date.strftime("%Y-%m-%d"),
                            "donor_id": "donor2",
                            "external_id": "8860a6b4-82e2-451c-aba2-a3129c38c0fc",
                            "name": "test1",
                            "priority_level": "Low",
                            "public_name": "Public2",
                            "sanger_sample_id": "sample2",
                            "species": "test " "species",
                            "supplier_name": "supplier2",
                            "taxon_id": "9606",
                        },
                    },
                ],
            },
        }
    }


def test_output_traction_message_can_generate_payload_for_mix_of_plate_and_tubes():
    my_date = datetime.utcnow()
    instance = OutputTractionMessage()

    request = instance.create_request()
    request.accession_number = "AN1234"
    request.container_barcode = "123"
    request.container_location = "A1"
    request.container_type = "wells"
    request.cost_code = "S1234"
    request.country_of_origin = "United Kingdom"
    request.date_of_sample_collection = my_date
    request.donor_id = "donor1"
    request.genome_size = "123,456,789"
    request.library_type = "library"
    request.priority_level = None
    request.public_name = "Public1"
    request.sample_name = "test1"
    request.sample_uuid = "8860a6b4-1234-451c-aba2-a3129c38c0fc"
    request.sanger_sample_id = "sample1"
    request.species = "test species"
    request.study_uuid = "dd490ee5-fd1d-456d-99fd-eb9d3861e014"
    request.supplier_name = "supplier1"
    request.taxon_id = "9606"

    request = instance.create_request()
    request.accession_number = "AN1235"
    request.container_barcode = "123"
    request.container_location = "B1"
    request.container_type = "wells"
    request.cost_code = "S4567"
    request.country_of_origin = "United Kingdom"
    request.date_of_sample_collection = my_date
    request.donor_id = "donor2"
    request.genome_size = None
    request.library_type = "library"
    request.priority_level = None
    request.public_name = "Public2"
    request.sample_name = "test2"
    request.sample_uuid = "8860a6b4-1235-451c-aba2-a3129c38c0fc"
    request.sanger_sample_id = "sample2"
    request.species = "test species"
    request.study_uuid = "dd490ee5-fd1d-456d-99fd-eb9d3861e014"
    request.supplier_name = "supplier2"
    request.taxon_id = "9606"

    request = instance.create_request()
    request.accession_number = "AN1236"
    request.container_barcode = "987"
    request.container_type = "tubes"
    request.cost_code = "S1234"
    request.country_of_origin = "United Kingdom"
    request.date_of_sample_collection = my_date
    request.donor_id = "donor3"
    request.genome_size = None
    request.library_type = "library"
    request.priority_level = "High"
    request.public_name = "Public3"
    request.sample_name = "test3"
    request.sample_uuid = "8860a6b4-1236-451c-aba2-a3129c38c0fc"
    request.sanger_sample_id = "sample3"
    request.species = "test species"
    request.study_uuid = "dd490ee5-fd1d-456d-99fd-eb9d3861e014"
    request.supplier_name = "supplier3"
    request.taxon_id = "9606"

    request = instance.create_request()
    request.accession_number = "AN1237"
    request.container_barcode = "876"
    request.container_type = "tubes"
    request.cost_code = "S4567"
    request.country_of_origin = "United Kingdom"
    request.date_of_sample_collection = my_date
    request.donor_id = "donor4"
    request.genome_size = "987,654,321"
    request.library_type = "library"
    request.priority_level = "Low"
    request.public_name = "Public4"
    request.sample_name = "test4"
    request.sample_uuid = "8860a6b4-1237-451c-aba2-a3129c38c0fc"
    request.sanger_sample_id = "sample4"
    request.species = "test species"
    request.study_uuid = "dd490ee5-fd1d-456d-99fd-eb9d3861e014"
    request.supplier_name = "supplier4"
    request.taxon_id = "9606"

    assert instance.payload() == {
        "data": {
            "type": "receptions",
            "attributes": {
                "source": "tol-lab-share.tol",
                "plates_attributes": [
                    {
                        "barcode": "123",
                        "type": "plates",
                        "wells_attributes": [
                            {
                                "position": "A1",
                                "request": {
                                    "cost_code": "S1234",
                                    "estimate_of_gb_required": "123,456,789",
                                    "external_study_id": "dd490ee5-fd1d-456d-99fd-eb9d3861e014",
                                    "library_type": "library",
                                },
                                "sample": {
                                    "accession_number": "AN1234",
                                    "country_of_origin": "United Kingdom",
                                    "date_of_sample_collection": my_date.strftime("%Y-%m-%d"),
                                    "donor_id": "donor1",
                                    "external_id": "8860a6b4-1234-451c-aba2-a3129c38c0fc",
                                    "name": "test1",
                                    "priority_level": None,
                                    "public_name": "Public1",
                                    "sanger_sample_id": "sample1",
                                    "species": "test " "species",
                                    "supplier_name": "supplier1",
                                    "taxon_id": "9606",
                                },
                            },
                            {
                                "position": "B1",
                                "request": {
                                    "cost_code": "S4567",
                                    "estimate_of_gb_required": None,
                                    "external_study_id": "dd490ee5-fd1d-456d-99fd-eb9d3861e014",
                                    "library_type": "library",
                                },
                                "sample": {
                                    "accession_number": "AN1235",
                                    "country_of_origin": "United Kingdom",
                                    "date_of_sample_collection": my_date.strftime("%Y-%m-%d"),
                                    "donor_id": "donor2",
                                    "external_id": "8860a6b4-1235-451c-aba2-a3129c38c0fc",
                                    "name": "test2",
                                    "priority_level": None,
                                    "public_name": "Public2",
                                    "sanger_sample_id": "sample2",
                                    "species": "test " "species",
                                    "supplier_name": "supplier2",
                                    "taxon_id": "9606",
                                },
                            },
                        ],
                    },
                ],
                "tubes_attributes": [
                    {
                        "barcode": "987",
                        "type": "tubes",
                        "request": {
                            "cost_code": "S1234",
                            "estimate_of_gb_required": None,
                            "external_study_id": "dd490ee5-fd1d-456d-99fd-eb9d3861e014",
                            "library_type": "library",
                        },
                        "sample": {
                            "accession_number": "AN1236",
                            "country_of_origin": "United Kingdom",
                            "date_of_sample_collection": my_date.strftime("%Y-%m-%d"),
                            "donor_id": "donor3",
                            "external_id": "8860a6b4-1236-451c-aba2-a3129c38c0fc",
                            "name": "test3",
                            "priority_level": "High",
                            "public_name": "Public3",
                            "sanger_sample_id": "sample3",
                            "species": "test " "species",
                            "supplier_name": "supplier3",
                            "taxon_id": "9606",
                        },
                    },
                    {
                        "barcode": "876",
                        "type": "tubes",
                        "request": {
                            "cost_code": "S4567",
                            "estimate_of_gb_required": "987,654,321",
                            "external_study_id": "dd490ee5-fd1d-456d-99fd-eb9d3861e014",
                            "library_type": "library",
                        },
                        "sample": {
                            "accession_number": "AN1237",
                            "country_of_origin": "United Kingdom",
                            "date_of_sample_collection": my_date.strftime("%Y-%m-%d"),
                            "donor_id": "donor4",
                            "external_id": "8860a6b4-1237-451c-aba2-a3129c38c0fc",
                            "name": "test4",
                            "priority_level": "Low",
                            "public_name": "Public4",
                            "sanger_sample_id": "sample4",
                            "species": "test " "species",
                            "supplier_name": "supplier4",
                            "taxon_id": "9606",
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
