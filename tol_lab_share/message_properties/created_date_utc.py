from .message_property import MessageProperty
import logging
from functools import cached_property
from datetime import datetime

logger = logging.getLogger(__name__)


class CreatedDateUtc(MessageProperty):
    @property
    def validators(self):
        return [self.check_is_float]

    @cached_property
    def value(self):
        logger.debug("MessageProperty::value")
        return datetime.fromtimestamp(self._input.value)
