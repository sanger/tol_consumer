import pytest
import statemachine  # type: ignore
from tol_lab_share.message_properties.message_property import MessageProperty
from tol_lab_share.state_machines.data_resolver import DataResolver
from tol_lab_share.messages.output_feedback_message import OutputFeedbackMessage


def build_property():
    return MessageProperty("test")


def test_data_resolver_state_machine_init_to_pending():
    instance = DataResolver(build_property())
    assert instance.state.is_pending is True


def test_data_resolver_state_machine_can_validate():
    instance = DataResolver(build_property())
    instance.validate()
    assert instance.state.is_valid is True

    # it can validate twice if we want
    instance.validate()
    instance.validate()
    assert instance.state.is_valid is True


def test_data_resolver_state_machine_can_resolve():
    instance = DataResolver(build_property())
    instance.validate()
    instance.resolve()
    assert instance.state.is_resolved is True

    # it can resolve twice
    instance.resolve()
    instance.resolve()
    assert instance.state.is_resolved is True

    # it can validate after resolve
    instance.validate()
    assert instance.state.is_resolved is True


def test_data_resolver_state_machine_cannot_transition_wrongly():
    instance = DataResolver(build_property())

    # cannot resolve without validate
    with pytest.raises(statemachine.exceptions.TransitionNotAllowed):
        instance.resolve()

    assert instance.state.is_pending is True

    # cannot obtain value without resolve
    with pytest.raises(statemachine.exceptions.TransitionNotAllowed):
        instance.value

    instance.validate()

    assert instance.state.is_valid is True

    # cannot obtain value without resolve
    with pytest.raises(statemachine.exceptions.TransitionNotAllowed):
        instance.value

    assert instance.state.is_valid is True

    instance.resolve()
    assert instance.state.is_resolved is True
    instance.value
    instance.validate()
    instance.resolve()
    instance.value
    assert instance.state.is_resolved is True


def test_data_resolver_validate_when_instance_not_valid_resolver_is_not_valid():
    # Not binary
    prop = build_property()
    prop._validators = [lambda: False]
    instance = DataResolver(prop)
    assert instance.validate() is False


def test_data_resolver_validate_when_valid_resolver_is_valid():
    instance = DataResolver(build_property())
    assert instance.validate() is True


def test_add_to_feedback_message_when_resolved():
    instance = DataResolver(build_property())
    feedback = OutputFeedbackMessage()

    instance.validate()
    instance.resolve()
    instance.add_to_feedback_message(feedback)
