from .message_property import MessageProperty
import logging
from typing import List, Callable

logger = logging.getLogger(__name__)


class DateSubmittedUTC(MessageProperty):
    """MessageProperty subclass to manage parsing of a valid Date submitted in UTC format provided by another
    MessageProperty. The date has to be a valid datetime.datetime instance.
    """

    @property
    def validators(self) -> List[Callable]:
        """Defines the list of validators"""
        return [self.check_is_date_utc]
