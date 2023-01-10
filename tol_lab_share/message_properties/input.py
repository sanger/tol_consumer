from .message_property import MessageProperty
from functools import cached_property
import logging

logger = logging.getLogger(__name__)


class Input(MessageProperty):
    def __init__(self, value):
        self._value = value
        self._errors = []
        self._properties = {}

    @cached_property
    def value(self):
        return self._value

    @property
    def validators(self):
        return []
