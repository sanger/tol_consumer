from tol_lab_share.messages.properties import MessageProperty
from typing import Callable


class StringValue(MessageProperty):
    """A simple string value. The value will be validated to be a string."""

    @property
    def validators(self) -> list[Callable]:
        """Validate the value to be a string."""
        return [self.check_is_string]
