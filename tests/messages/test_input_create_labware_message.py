from tol_lab_share.messages import InputCreateLabwareMessage, OutputFeedbackMessage
from lab_share_lib.processing.rabbit_message import RabbitMessage
import pytest

@pytest.fixture
def subject(decoded_rabbit_message):
    return InputCreateLabwareMessage(decoded_rabbit_message)

def test_input_create_labware_message_can_create_instance(subject):
    assert subject != None

def test_input_create_labware_message_can_validate_when_valid(subject):
    assert subject.validate() == True

def test_input_create_labware_message_can_validate_when_invalid(decoded_rabbit_message):
    decoded_rabbit_message.message['messageUuid'] = '1234'
    instance = InputCreateLabwareMessage(decoded_rabbit_message)
    assert instance.validate() == False

def test_input_create_labware_message_can_add_to_feedback_message(subject):
    feedback_message = OutputFeedbackMessage()
    assert subject.add_to_feedback_message(feedback_message) == True