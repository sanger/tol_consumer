import pytest
import statemachine  # type: ignore
from tol_lab_share.messages.input_create_labware_message import InputCreateLabwareMessage
from tol_lab_share.messages.output_feedback_message import OutputFeedbackMessage
from tol_lab_share.data_resolvers.data_resolver import DataResolver


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
    assert len(instance.errors) == 7


def test_input_create_labware_message_cannot_add_to_feedback_message_if_valid_but_not_resolved(
    valid_create_labware_message,
):

    subject = DataResolver(InputCreateLabwareMessage(valid_create_labware_message))
    feedback_message = OutputFeedbackMessage()

    assert subject.state.is_pending
    assert subject.validate() is True
    assert subject.state.is_valid

    with pytest.raises(statemachine.exceptions.TransitionNotAllowed):
        subject.add_to_feedback_message(feedback_message)


def test_input_create_labware_message_can_add_to_feedback_message_if_invalid(invalid_create_labware_message):
    subject = DataResolver(InputCreateLabwareMessage(invalid_create_labware_message))
    feedback_message = OutputFeedbackMessage()

    assert subject.state.is_pending
    assert subject.validate() is False
    assert subject.state.is_invalid

    subject.resolve()
    subject.add_to_feedback_message(feedback_message)
    assert len(feedback_message.errors) > 0


def test_input_create_labware_message_can_add_to_feedback_message_if_resolved(valid_create_labware_message):
    subject = DataResolver(InputCreateLabwareMessage(valid_create_labware_message))
    subject.validate()
    subject.resolve()
    feedback_message = OutputFeedbackMessage()

    assert feedback_message.source_message_uuid is None

    subject.add_to_feedback_message(feedback_message)

    assert feedback_message.source_message_uuid == "b01aa0ad-7b19-4f94-87e9-70d74fb8783c"
