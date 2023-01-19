from .message_property import MessageProperty
from functools import cached_property
import logging

logger = logging.getLogger(__name__)


class Input(MessageProperty):
    @cached_property
    def value(self):
        return self._input

    @property
    def validators(self):
        return []
