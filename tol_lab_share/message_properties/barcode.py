import logging
from .message_property import MessageProperty
from tol_lab_share import error_codes

logger = logging.getLogger(__name__)


class Barcode(MessageProperty):
    @property
    def default_error_code(self):
        return error_codes.ERROR_3_BARCODE_NOT_STRING

    @property
    def validators(self):
        return [self.check_is_string]
