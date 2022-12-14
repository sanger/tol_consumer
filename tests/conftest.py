import pytest
import logging
import logging.config
from tol_lab_share.helpers import get_config
from lab_share_lib.processing.rabbit_message import RabbitMessage
from lab_share_lib.constants import (
    RABBITMQ_HEADER_KEY_SUBJECT,
    RABBITMQ_HEADER_KEY_VERSION,
)
from tol_lab_share.constants import (
    INPUT_CREATE_LABWARE_MESSAGE_MESSAGE_UUID, 
    INPUT_CREATE_LABWARE_MESSAGE_CREATED_DATE_UTC, INPUT_CREATE_LABWARE_MESSAGE_LABWARE
)
from data.create_labware_message import TEST_CREATE_LABWARE_MSG_OBJECT

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
DECODED_LIST = [TEST_CREATE_LABWARE_MSG_OBJECT]
# DECODED_LIST = [{
#     INPUT_CREATE_LABWARE_MESSAGE_MESSAGE_UUID: '1234', 
#     INPUT_CREATE_LABWARE_MESSAGE_CREATED_DATE_UTC: '1234',
#     INPUT_CREATE_LABWARE_MESSAGE_LABWARE: '1234'
# }]


@pytest.fixture
def rabbit_message():
    return RabbitMessage(HEADERS, ENCODED_BODY)

@pytest.fixture
def decoder():
    decoder = MagicMock()
    decoder.decode.return_value = DECODED_LIST

    return decoder


@pytest.fixture
def decoded_rabbit_message(rabbit_message, decoder):
    m = RabbitMessage(HEADERS, ENCODED_BODY)
    m.decode(decoder)

    return m

