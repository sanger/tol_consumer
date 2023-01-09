from .message_property import MessageProperty
from tol_lab_share.messages.output_feedback_message import OutputFeedbackMessage
from uuid import UUID
from tol_lab_share import error_codes

from typing import Optional, Any
from functools import cached_property
import logging

logger = logging.getLogger(__name__)


class Uuid(MessageProperty):
    @property
    def validators(self):
        return [self.check_is_binary, self.check_is_uuid]

    def check_is_binary(self):
        logger.debug("Uuid::check_is_binary")
        try:
            self._input.decode("utf-8")
            return True
        except AttributeError:
            pass
        self.add_error(error_codes.ERROR_1_UUID_NOT_BINARY)
        return False

    def check_is_uuid(self):
        logger.debug("Uuid::check_is_uuid")
        try:
            str_rep = self._input.decode("utf-8")
            uuid_obj = UUID(str_rep, version=4)
            if str(uuid_obj) == str(str_rep):
                return True
        except ValueError:
            pass
        except AttributeError:
            pass
        self.add_error(error_codes.ERROR_2_UUID_NOT_RIGHT_FORMAT)
        return False

    def add_to_feedback_message(self, feedback_message: OutputFeedbackMessage) -> None:
        logger.debug("Uuid::add_to_feedback_message")
        self.add_errors_to_feedback_message(feedback_message)
        feedback_message.source_message_uuid = self.value
        if feedback_message.operation_was_error_free is None:
            feedback_message.operation_was_error_free = True

    @cached_property
    def value(self) -> Optional[Any]:
        logger.debug("Uuid::value")
        return self._input.decode("utf-8")
