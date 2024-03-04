from tol_lab_share.messages.properties import MessageProperty
from functools import cached_property


class Value(MessageProperty):
    """MessageProperty subclass to wrap any value, providing a MessageProperty-like access to the value."""

    @cached_property
    def value(self):
        return self._input
