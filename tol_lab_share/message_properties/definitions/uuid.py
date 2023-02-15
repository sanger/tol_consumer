from .message_property import MessageProperty
from uuid import UUID
from tol_lab_share import error_codes

from typing import Optional, Any
from functools import cached_property
import logging
from typing import List, Callable

logger = logging.getLogger(__name__)


class Uuid(MessageProperty):
    """MessageProperty subclass to manage parsing of a valid uuid provided by another
    MessageProperty.
    The uuid has to be binary defined in version UUID v4 and encoded using utf-8."""

    @property
    def validators(self) -> List[Callable]:
        """Defines the list of validators"""
        return [self.check_is_binary, self.check_is_uuid]

    def check_is_binary(self) -> bool:
        """Checks that the input is a utf-8 string and returns it result.
        Triggers and error if it is not"""
        logger.debug("Uuid::check_is_binary")
        if not self._input.validate():
            return False
        try:
            self._input.value.decode("utf-8")
            return True
        except AttributeError:
            pass
        self.trigger_error(error_codes.ERROR_1_UUID_NOT_BINARY)
        return False

    def check_is_uuid(self):
        """Checks that the input is a UUID v4 and returns it result.
        Triggers and error if it is not"""
        logger.debug("Uuid::check_is_uuid")
        if not self._input.validate():
            return False

        try:
            str_rep = self._input.value.decode("utf-8")
            uuid_obj = UUID(str_rep)
            if str(uuid_obj) == str(str_rep):
                return True
        except ValueError:
            pass
        except AttributeError:
            pass
        self.trigger_error(error_codes.ERROR_2_UUID_NOT_RIGHT_FORMAT, text=f"input: {self._input.value}")
        return False

    @cached_property
    def value(self) -> Optional[Any]:
        """Returns the string representation of the uuid"""
        return self._input.value.decode("utf-8")
