from .message_property import MessageProperty
from tol_lab_share import error_codes


class CommonName(MessageProperty):
    @property
    def default_error_code(self):
        return error_codes.ERROR_2_NOT_STRING

    @property
    def validators(self):
        return [self.check_is_string]
