from tol_lab_share.messages.output_feedback_message import OutputFeedbackMessage
from typing import List
from tol_lab_share.error_codes import ErrorCode
from functools import cached_property


class MessageProperty:
    def __init__(self, input):
        self._input = input
        self._errors = []
        self.set_validators()

    def validate(self):
        return all([validator() for validator in self._validators])

    @cached_property
    def value(self):
        return self._input

    def resolve(self):
        pass

    def add_to_feedback_message(self, feedback_message: OutputFeedbackMessage) -> None:
        self.add_errors_to_feedback_message(feedback_message)

    @property
    def errors(self) -> List[ErrorCode]:
        return self._errors

    def add_errors_to_feedback_message(self, feedback_message: OutputFeedbackMessage) -> None:
        for error in self.errors:
            feedback_message.add_error_code(error)

    def set_validators(self):
        self._validators = []

    def check_is_string(self):
        return isinstance(self._input, str)
