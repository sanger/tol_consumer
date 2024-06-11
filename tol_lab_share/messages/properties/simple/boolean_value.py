from tol_lab_share.messages.properties import MessageProperty
from typing import Callable


class BooleanValue(MessageProperty):
    """A simple boolean value. The value will be validated to be a boolean."""

    @property
    def validators(self) -> list[Callable]:
        """Validate the value to be a boolean."""
        return [self.check_is_boolean]
