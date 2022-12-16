from tol_lab_share.messages.output_feedback_message import OutputFeedbackMessage
from typing import Optional, Any, List
from tol_lab_share.state_machines.data_resolution import DataResolution
from functools import cached_property
from tol_lab_share.error_codes import ErrorCode


class MessageProperty:
    def __init__(self, input):
        self._input = input
        self._errors = []
        self.set_validators()
        self._value = None
        self.state = DataResolution()

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
    def errors(self) -> List[ErrorCode]:
        return self._errors

    @cached_property
    def value(self) -> Optional[Any]:
        self.state.retrieve_value()

        return self._input

    def set_validators(self):
        self._validators = []

    def add_to_feedback_message(self, feedback_message: OutputFeedbackMessage) -> None:
        pass
