from tol_lab_share.messages.properties import MessageProperty
from typing import Callable


class StringValue(MessageProperty):
    """A simple string value. The value will be validated to be a string."""

    def __init__(self, input: MessageProperty, optional: bool = False):
        super().__init__(input)
        self._optional = optional

    @property
    def validators(self) -> list[Callable]:
        """Validate the value to be a string."""
        return [self.string_checker(optional=self._optional)]
