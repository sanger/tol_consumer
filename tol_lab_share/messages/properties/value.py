from .message_property import MessageProperty
from functools import cached_property
import logging

logger = logging.getLogger(__name__)


class Value(MessageProperty):
    """MessageProperty subclass to wrap any value, providing a MessageProperty-like access to the value."""

    @cached_property
    def value(self):
        return self._input
