from .message_property import MessageProperty
import logging
from typing import List, Callable
from functools import cached_property
from typing import Any

logger = logging.getLogger(__name__)


class DateUtc(MessageProperty):
    """MessageProperty subclass to manage parsing of a valid date provided by another
    MessageProperty. The date has to be a valid datetime.datetime instance.
    """

    @property
    def validators(self) -> List[Callable]:
        """Defines the list of validators"""
        return [self.check_is_date_utc]

    @cached_property
    def value(self) -> Any:
        if type(self._input.value) is tuple:
            return self._input.value[0]
        return self._input.value
