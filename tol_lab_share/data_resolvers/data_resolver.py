from tol_lab_share.messages.output_feedback_message import OutputFeedbackMessage
from typing import Optional, Any
from functools import cached_property
from tol_lab_share.data_resolvers.data_resolver_state_machine import DataResolverStateMachine
from tol_lab_share.data_resolvers.data_resolver_interface import DataResolverInterface


class DataResolver(DataResolverInterface):
    def __init__(self, instance):
        self._instance = instance
        self._errors = []
        self.set_validators()
        self._value = None
        self.state = DataResolverStateMachine()

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
