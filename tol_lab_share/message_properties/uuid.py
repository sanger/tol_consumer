from .message_property import MessageProperty
from tol_lab_share.messages.output_feedback_message import OutputFeedbackMessage
from uuid import UUID
from tol_lab_share.message_properties.exceptions import (
    InvalidInputMessageProperty,
    ValueNotReadyForMessageProperty,
    ErrorWhenObtainingMessageProperty,
)


class Uuid(MessageProperty):
    def set_validators(self):
        self._validators = [self.check_is_binary, self.check_is_uuid]

    def check_is_binary(self):
        try:
            self._input.decode("utf-8")
        except AttributeError:
            self._errors.append("The string for uuid is not a binary")
            return False
        return True

    def check_is_uuid(self):
        try:
            str_rep = self._input.decode("utf-8")
            uuid_obj = UUID(str_rep, version=4)
        except ValueError:
            self._errors.append("The string is not a uuid")
            return False
        except AttributeError:
            self._errors.append("The string is not a binary")
            return False
        return str(uuid_obj) == str(str_rep)

    def add_to_feedback_message(self, feedback_message: OutputFeedbackMessage) -> None:
        if self.state.is_resolved:
            feedback_message.source_message_uuid = self.value
            if feedback_message.operation_was_error_free is None:
                feedback_message.operation_was_error_free = True
        else:
            feedback_message.operation_was_error_free = False
            raise ValueNotReadyForMessageProperty()
