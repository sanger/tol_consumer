from tol_lab_share.messages.output_feedback_message import OutputFeedbackMessage
from typing import Optional, Any
from functools import cached_property

from statemachine import StateMachine, State  # type: ignore


class DataResolverDefinition(StateMachine):
    # states
    pending = State("pending", initial=True)
    validating = State("validating")
    valid = State("valid")
    invalid = State("invalid")
    resolving = State("resolving")
    resolved = State("resolved")
    error = State("error")

    # transitions
    performing_validation = (
        pending.to(validating) | valid.to(validating) | invalid.to(validating) | resolved.to(resolved)
    )
    validation_passed = validating.to(valid) | valid.to(valid) | invalid.to(valid) | resolved.to(resolved)
    validation_failed = validating.to(invalid) | invalid.to(invalid) | valid.to(invalid)
    request_resolution = valid.to(resolving) | resolved.to(resolved)
    resolution_successful = resolving.to(resolved) | resolved.to(resolved)
    resolution_failed = resolving.to(error) | resolved.to(error)
    retrieve_value = resolved.to(resolved)
    retrieve_feedback = invalid.to(invalid) | resolved.to(resolved) | error.to(error)


class DataResolver:
    def __init__(self, instance):
        self._instance = instance
        self._errors = []
        self.set_validators()
        self._value = None
        self.state = DataResolverDefinition()

    def validate(self):
        self.state.performing_validation()
        result = self._instance.validate()
        if result:
            self.state.validation_passed()
        else:
            self.state.validation_failed()
        return result

    def resolve(self):
        self.state.request_resolution()
        self._instance.resolve()
        self.state.resolution_successful()

    @property
    def errors(self) -> Any:
        return self._instance.errors

    @cached_property
    def value(self) -> Optional[Any]:
        self.state.retrieve_value()
        return self._instance.value

    def set_validators(self):
        self._validators = []

    def add_to_feedback_message(self, feedback_message: OutputFeedbackMessage) -> None:
        self.state.retrieve_feedback()
        feedback_message.operation_was_error_free = self.state.is_resolved and len(self.errors) == 0
        self._instance.add_to_feedback_message(feedback_message)
