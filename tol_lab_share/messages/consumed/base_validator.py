from abc import ABC, abstractmethod
import logging
from uuid import UUID

from tol_lab_share import error_codes
from tol_lab_share.error_codes import ErrorCode

from .message_field import MessageField

LOGGER = logging.getLogger(__name__)


class BaseValidator(ABC):
    def __init__(self) -> None:
        super().__init__()
        self._errors: list[ErrorCode] = []

    @abstractmethod
    def validate(self) -> bool:
        ...

    @property
    def errors(self) -> list[ErrorCode]:
        """Gets the list of errors that occurred during validation.

        Returns:
            list[ErrorCode]: A list of errors that occurred during validation.
        """
        return self._errors.copy()

    def _check_is_uuid(self, field: MessageField) -> bool:
        """Checks that the given value is a UUID v4.

        Args:
            value (str): The string value to check.
        """
        LOGGER.debug("BaseValidator::check_is_uuid")
        try:
            value = str(field.value)
            uuid_obj = UUID(value)
            if str(uuid_obj) != value:
                raise ValueError("Value is not a version 4 UUID.")
        except (ValueError, AttributeError):
            self._trigger_error(error_codes.ERROR_2_UUID_NOT_RIGHT_FORMAT, text=f"input: {value}", field=field.name)
            return False

        return True

    def _reset_errors(self) -> None:
        """Resets the list of errors."""
        self._errors = []

    def _trigger_error(self, error_code: ErrorCode, text: str | None = None, field: str | None = None) -> None:
        """Triggers the given error and adds it to the list of errors.

        Args:
            error_code (ErrorCode): The error code to trigger.
            text (str | None, optional): The text to include in the error. Defaults to None.
            field (str | None, optional): The field name that caused the error. Defaults to None.
        """
        self._errors.append(error_code.trigger(text=text, field=field))
