import pytest
import logging
import logging.config
from tol_lab_share.helpers import get_config
from lab_share_lib.processing.rabbit_message import RabbitMessage
from lab_share_lib.constants import (
    RABBITMQ_HEADER_KEY_SUBJECT,
    RABBITMQ_HEADER_KEY_VERSION,
)
from data.examples_create_labware_messages import TEST_CREATE_LABWARE_MSG_OBJECT, TEST_INVALID_CREATE_LABWARE_MSG_OBJECT

from unittest.mock import MagicMock


CONFIG = get_config("tol_lab_share.config.test")
logging.config.dictConfig(CONFIG.LOGGING)


@pytest.fixture
def config():
    return CONFIG


HEADERS = {
    RABBITMQ_HEADER_KEY_SUBJECT: "a-subject",
    RABBITMQ_HEADER_KEY_VERSION: "3",
}

ENCODED_BODY = "Encoded body"
VALID_DECODED_LIST = [TEST_CREATE_LABWARE_MSG_OBJECT]
INVALID_DECODED_LIST = [TEST_INVALID_CREATE_LABWARE_MSG_OBJECT]

# DECODED_LIST = [{
#     INPUT_CREATE_LABWARE_MESSAGE_MESSAGE_UUID: '1234',
#     INPUT_CREATE_LABWARE_MESSAGE_CREATED_DATE_UTC: '1234',
#     INPUT_CREATE_LABWARE_MESSAGE_LABWARE: '1234'
# }]


@pytest.fixture
def unchecked_create_labware_message():
    return RabbitMessage(HEADERS, ENCODED_BODY)


@pytest.fixture
def valid_decoder():
    decoder = MagicMock()
    decoder.decode.return_value = VALID_DECODED_LIST

    return decoder


@pytest.fixture
def invalid_decoder():
    decoder = MagicMock()
    decoder.decode.return_value = INVALID_DECODED_LIST

    return decoder


@pytest.fixture
def valid_create_labware_message(unchecked_create_labware_message, valid_decoder):
    unchecked_create_labware_message.decode(valid_decoder)

    return unchecked_create_labware_message


@pytest.fixture
def invalid_create_labware_message(unchecked_create_labware_message, invalid_decoder):
    unchecked_create_labware_message.decode(invalid_decoder)

    return unchecked_create_labware_message


@pytest.fixture
def mocked_response():
    return {
        "data": {
            "id": "52",
            "type": "receptions",
            "links": {"self": "http://localhost:3000/v1/receptions/52"},
            "attributes": {"source": "traction-ui.sequencescape"},
        }
    }
