from tol_lab_share.messages.properties import MessageProperty
from typing import Callable


class FloatValue(MessageProperty):
    """A simple float value. The value will be validated to be a float."""

    @property
    def validators(self) -> list[Callable]:
        """Validate the value to be a float."""
        return [self.check_is_float]
