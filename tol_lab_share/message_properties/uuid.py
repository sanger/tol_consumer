from .message_property import MessageProperty
from tol_lab_share.messages.output_feedback_message import OutputFeedbackMessage
from uuid import UUID
from tol_lab_share import error_codes

from typing import Optional, Any
from functools import cached_property


class Uuid(MessageProperty):
    def set_validators(self):
        self._validators = [self.check_is_binary, self.check_is_uuid]

    def check_is_binary(self):
        try:
            self._input.decode("utf-8")
            return True
        except AttributeError:
            pass
        self.errors.append(error_codes.ERROR_1_UUID_NOT_BINARY)
        return False

    def check_is_uuid(self):
        try:
            str_rep = self._input.decode("utf-8")
            uuid_obj = UUID(str_rep, version=4)
            if str(uuid_obj) == str(str_rep):
                return True
        except ValueError:
            pass
        except AttributeError:
            pass
        self.errors.append(error_codes.ERROR_2_UUID_NOT_RIGHT_FORMAT)
        return False

    def add_to_feedback_message(self, feedback_message: OutputFeedbackMessage) -> None:
        self.add_errors_to_feedback_message(feedback_message)
        feedback_message.source_message_uuid = self.value
        if feedback_message.operation_was_error_free is None:
            feedback_message.operation_was_error_free = True

    @cached_property
    def value(self) -> Optional[Any]:
        return self._input.decode("utf-8")
