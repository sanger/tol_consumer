from .message_property import MessageProperty
from tol_lab_share import error_codes


class Concentration(MessageProperty):
    @property
    def default_error_code(self):
        return error_codes.ERROR_3_NOT_INTEGER

    @property
    def validators(self):
        return [self.check_is_integer]
