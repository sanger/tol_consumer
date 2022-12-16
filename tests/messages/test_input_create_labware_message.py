import pytest
import statemachine
from tol_lab_share.messages import InputCreateLabwareMessage, OutputFeedbackMessage
from tol_lab_share.message_properties.exceptions import ValueNotReadyForMessageProperty


def test_input_create_labware_message_can_create_instance(valid_create_labware_message):
    subject = InputCreateLabwareMessage(valid_create_labware_message)
    assert subject is not None


def test_input_create_labware_message_can_validate_when_valid(valid_create_labware_message):
    subject = InputCreateLabwareMessage(valid_create_labware_message)
    assert subject.validate() is True
    assert len(subject.errors) == 0


def test_input_create_labware_message_can_validate_when_invalid(invalid_create_labware_message):
    instance = InputCreateLabwareMessage(invalid_create_labware_message)
    assert instance.validate() is False
    assert len(instance.errors) == 1


def test_input_create_labware_message_cannot_add_to_feedback_message_if_not_evaluated(invalid_create_labware_message):

    subject = InputCreateLabwareMessage(invalid_create_labware_message)
    feedback_message = OutputFeedbackMessage()

    # Not validated yet
    with pytest.raises(statemachine.exceptions.TransitionNotAllowed):
        subject.add_to_feedback_message(feedback_message)

    assert subject.state.is_pending
    assert subject.validate() is False
    assert subject.state.is_invalid

    subject.add_to_feedback_message(feedback_message)
    assert len(feedback_message.errors) > 0


def test_input_create_labware_message_cannot_add_to_feedback_message_if_resolved(valid_create_labware_message):
    subject = InputCreateLabwareMessage(valid_create_labware_message)
    subject.validate()
    subject.resolve()
    feedback_message = OutputFeedbackMessage()
    assert subject.add_to_feedback_message(feedback_message) is True
