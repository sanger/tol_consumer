from .message_property import MessageProperty
from tol_lab_share import error_codes


class Barcode(MessageProperty):
    def set_validators(self):
        self._validators = [self.check_barcode_is_string]

    def check_barcode_is_string(self):
        result = self.check_is_string()
        if not result:
            self.errors.append(error_codes.ERROR_3_BARCODE_NOT_STRING)
        return result
