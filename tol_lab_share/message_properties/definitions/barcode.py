import logging
from .message_property import MessageProperty

logger = logging.getLogger(__name__)


class Barcode(MessageProperty):
    """MessageProperty subclass to manage parsing of a valid barcode string provided by another
    MessageProperty.
    The barcode has to be a valid string.
    Eg: 'testbarcode'
    """

    @property
    def validators(self):
        return [self.check_is_string]
