import logging
from .message_property import MessageProperty
from tol_lab_share import error_codes

logger = logging.getLogger(__name__)


class Barcode(MessageProperty):
    def set_validators(self):
        self._validators = [self.check_barcode_is_string]

    def check_barcode_is_string(self):
        logger.debug("Barcode::check_barcode_is_string")
        result = self.check_is_string()
        if not result:
            self.errors.append(error_codes.ERROR_3_BARCODE_NOT_STRING)
        return result
