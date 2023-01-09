import logging
from .message_property import MessageProperty

logger = logging.getLogger(__name__)


class Barcode(MessageProperty):
    @property
    def validators(self):
        return [self.check_is_string]
