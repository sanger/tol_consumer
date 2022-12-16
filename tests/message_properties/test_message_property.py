import pytest
import statemachine  # type: ignore
from tol_lab_share.message_properties.message_property import MessageProperty


def test_message_property_state_machine_init_to_pending():
    instance = MessageProperty("1234")
    assert instance.state.is_pending is True


def test_message_property_state_machine_can_validate():
    instance = MessageProperty("1234")
    instance.validate()
    assert instance.state.is_valid is True

    # it can validate twice if we want
    instance.validate()
    instance.validate()
    assert instance.state.is_valid is True


def test_message_property_state_machine_can_resolve():
    instance = MessageProperty("1234")
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


def test_message_property_state_machine_cannot_transition_wrongly():
    instance = MessageProperty("1234")

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
