from tol_lab_share.messages.output_feedback_message import OutputFeedbackMessage
from typing import Optional, Any
from tol_lab_share.message_properties.exceptions import (
    InvalidInputMessageProperty,
    ValueNotReadyForMessageProperty,
    ErrorWhenObtainingMessageProperty,
)
from functools import cached_property

from statemachine import StateMachine, State


class MessagePropertyStateMachine(StateMachine):
    # states
    pending = State("pending", initial=True)
    valid = State("valid")
    invalid = State("invalid")
    resolving = State("resolving")
    resolved = State("resolved")
    error = State("error")

    # transitions
    validation_passed = pending.to(valid)
    validation_failed = pending.to(invalid)
    request_resolution = valid.to(resolving)
    resolution_successful = resolving.to(resolved)
    resolution_failed = resolving.to(error)


class MessageProperty:
    def __init__(self, input):
        self._input = input
        self._errors = []
        self.set_validators()
        self._value = None
        self.state = MessagePropertyStateMachine()

    def validate(self):
        result = all([validator() for validator in self._validators])

        if result:
            self.state.validation_passed()
        else:
            self.state.validation_failed()

        return result

    def resolve(self):
        self.state.request_resolution()
        self.state.resolution_successful()

    @property
    def value(self) -> Optional[Any]:
        if self.state.is_resolved:
            return self._value
        else:
            raise ValueNotReadyForMessageProperty()

    def set_validators(self):
        self._validators = []

    def add_to_feedback_message(self, feedback_message: OutputFeedbackMessage) -> None:
        pass
