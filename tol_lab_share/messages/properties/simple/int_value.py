from tol_lab_share.messages.properties import MessageProperty
from typing import Callable


class IntValue(MessageProperty):
    """A simple integer value. The value will be validated to be a int."""

    def __init__(self, input: MessageProperty, optional: bool = False):
        super().__init__(input)
        self._optional = optional

    @property
    def validators(self) -> list[Callable]:
        """Validate the value to be a integer."""
        return [self.integer_checker(optional=self._optional)]
