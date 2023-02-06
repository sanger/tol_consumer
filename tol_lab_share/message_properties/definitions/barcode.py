import logging
from .message_property import MessageProperty
from typing import List, Callable

logger = logging.getLogger(__name__)


class Barcode(MessageProperty):
    """MessageProperty subclass to manage parsing of a valid barcode string provided by another
    MessageProperty.
    The barcode has to be a valid string.
    Eg: 'testbarcode'
    """

    @property
    def validators(self) -> List[Callable]:
        """Defines the list of validators"""
        return [self.check_is_string]
