import logging
from ...messages.properties.message_property import MessageProperty
from typing import Callable

logger = logging.getLogger(__name__)


class Barcode(MessageProperty):
    """MessageProperty subclass to manage parsing of a valid barcode string provided by another
    MessageProperty.
    The barcode has to be a valid string.
    Eg: 'testbarcode'
    """

    @property
    def validators(self) -> list[Callable]:
        """Defines the list of validators"""
        return [self.check_is_string]
