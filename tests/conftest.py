import logging
import logging.config
from datetime import datetime
from unittest.mock import MagicMock

import pytest
from tests.data.example_bioscan_pool_xp_to_traction_messages import (
    TEST_VALID_BIOSCAN_POOL_XP_TO_TRACTION_MSG_OBJECT,
    TEST_INVALID_BIOSCAN_POOL_XP_TO_TRACTION_MSG_OBJECT,
)
from tests.data.example_create_labware_messages import (
    TEST_VALID_CREATE_LABWARE_MSG_OBJECT,
    TEST_INVALID_CREATE_LABWARE_MSG_OBJECT,
)
from lab_share_lib.constants import RABBITMQ_HEADER_KEY_SUBJECT, RABBITMQ_HEADER_KEY_VERSION
from lab_share_lib.processing.rabbit_message import RabbitMessage

from tol_lab_share.helpers import get_config
from tol_lab_share.messages.rabbit.published import CreateLabwareFeedbackMessage

CONFIG = get_config("tol_lab_share.config.test")
logging.config.dictConfig(CONFIG.LOGGING)


@pytest.fixture
def config():
    return CONFIG


HEADERS = {
    RABBITMQ_HEADER_KEY_SUBJECT: "a-subject",
    RABBITMQ_HEADER_KEY_VERSION: "3",
}


@pytest.fixture
def generic_rabbit_message():
    return RabbitMessage(HEADERS, "Generic Body")


def mock_decoder(message_object):
    decoder = MagicMock()
    decoder.decode.return_value = [message_object]

    return decoder


@pytest.fixture
def valid_bioscan_pool_xp_to_traction_message(generic_rabbit_message):
    decoder = mock_decoder(TEST_VALID_BIOSCAN_POOL_XP_TO_TRACTION_MSG_OBJECT)
    generic_rabbit_message.decode(decoder)

    return generic_rabbit_message


@pytest.fixture
def invalid_bioscan_pool_xp_to_traction_message(generic_rabbit_message):
    decoder = mock_decoder(TEST_INVALID_BIOSCAN_POOL_XP_TO_TRACTION_MSG_OBJECT)
    generic_rabbit_message.decode(decoder)

    return generic_rabbit_message


@pytest.fixture
def valid_create_labware_message(generic_rabbit_message):
    decoder = mock_decoder(TEST_VALID_CREATE_LABWARE_MSG_OBJECT)
    generic_rabbit_message.decode(decoder)

    return generic_rabbit_message


@pytest.fixture
def invalid_create_labware_message(generic_rabbit_message):
    decoder = mock_decoder(TEST_INVALID_CREATE_LABWARE_MSG_OBJECT)
    generic_rabbit_message.decode(decoder)

    return generic_rabbit_message


@pytest.fixture
def traction_success_creation_response():
    return {
        "data": {
            "id": "52",
            "type": "receptions",
            "links": {"self": "http://localhost:3000/v1/receptions/52"},
            "attributes": {"source": "traction-ui.sequencescape"},
        }
    }


@pytest.fixture()
def traction_qc_success_response():
    return {
        "data": {
            "id": "10",
            "type": "qc_receptions",
            "links": {"self": "http://localhost:3000/v1/qc_receptions/10"},
            "attributes": {"source": "tol-lab-share.tol"},
        }
    }


@pytest.fixture()
def valid_feedback_message():
    instance = CreateLabwareFeedbackMessage()
    instance.count_of_total_samples = 0
    instance.count_of_valid_samples = 0
    instance.source_message_uuid = b"b01aa0ad-7b19-4f94-87e9-70d74fb8783c"
    instance.operation_was_error_free = True
    return instance


@pytest.fixture
def taxonomy_record():
    return {
        "taxId": "9600",
        "scientificName": "Pongo pygmaeus",
        "commonName": "Bornean orangutan",
        "formalName": "true",
        "rank": "species",
        "division": "MAM",
        "lineage": (
            "Eukaryota; Metazoa; Chordata; Craniata; Vertebrata; Euteleostomi; "
            "Mammalia; Eutheria; Euarchontoglires; Primates; Haplorrhini; "
            "Catarrhini; Hominidae; Pongo; "
        ),
        "geneticCode": "1",
        "mitochondrialGeneticCode": "2",
        "submittable": "true",
        "binomial": "true",
    }


@pytest.fixture
def valid_create_labware_sample():
    return {
        "accessionNumber": "EE1234",
        "commonName": "Mus Musculus",
        "concentration": "5",
        "costCode": "S1234",
        "countryOfOrigin": "United Kingdom",
        "dateSubmittedUTC": datetime.utcnow(),
        "donorId": "cichlid_pacbio8196429",
        "finalNanoDrop": "150",
        "finalNanoDrop230": "200",
        "finalNanoDrop280": "200",
        "genomeSize": "14",
        "libraryType": "Library1",
        "location": "A01",
        "postSPRIConcentration": "9",
        "postSPRIVolume": "10",
        "priorityLevel": "Medium",
        "publicName": "SamplePublicName1",
        "sampleCollectionDateUtc": datetime.utcnow(),
        "sampleUuid": "dd490ee5-fd1d-456d-99fd-eb9d3861e0f6".encode(),
        "sangerSampleId": "cichlid_pacbio8196429",
        "shearedFemtoFragmentSize": "8",
        "shearingAndQCComments": "",
        "studyUuid": "dd490ee5-fd1d-456d-99fd-eb9d3861e014".encode(),
        "supplierSampleName": "SampleSupplied1",
        "taxonId": "10090",
        "volume": "5",
    }


@pytest.fixture
def invalid_create_labware_sample():
    return {
        "accessionNumber": "EE1234",
        "commonName": 1234,
        "concentration": "ee5",
        "costCode": 1234,
        "countryOfOrigin": 1234,
        "dateSubmittedUTC": datetime.utcnow(),
        "donorId": 1234,
        "finalNanoDrop": "150",
        "finalNanoDrop230": 200,
        "finalNanoDrop280": 200,
        "genomeSize": "14",
        "libraryType": 1234,
        "location": "A001",
        "postSPRIConcentration": "9",
        "postSPRIVolume": "10",
        "priorityLevel": "Medium",
        "publicName": "1234",
        "sampleCollectionDateUtc": datetime.utcnow(),
        "sampleUuid": b"dd490ee5-fd1d-456d-99fd-eb9d3861e0f6",
        "sangerSampleId": 1234,
        "shearedFemtoFragmentSize": "8",
        "shearingAndQCComments": "",
        "studyUuid": "dd490ee5-fd1d-456d-99fd-eb9d3861e014",
        "supplierSampleName": "1234",
        "taxonId": "ee10090",
        "volume": "ee5",
    }


def read_file(filename):
    with open(filename, "r") as file:
        return file.read()


@pytest.fixture
def feedback_schema_json():
    return read_file("./schemas/create-labware-feedback/1-create-labware-feedback.avsc")
