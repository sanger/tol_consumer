from .message_property import MessageProperty
from functools import cached_property
from tol_lab_share import error_codes
import logging
from tol_lab_share.message_properties.definitions.input import Input

logger = logging.getLogger(__name__)


class DictInput(MessageProperty):
    def __init__(self, input, key):
        super().__init__(input)
        if not isinstance(input, MessageProperty):
            self._input = Input(input)
        else:
            self._input = input
        self._key = key

    @property
    def validators(self):
        return [self.check_has_key]

    def check_has_key(self):
        if not self._input.validate():
            self.trigger_error(error_codes.ERROR_11_PARENT_DICT_WRONG)
            return False

        if not self.check_iterable():
            return False

        if self._key not in self._input.value:
            self.trigger_error(error_codes.ERROR_10_DICT_WRONG_KEY, text=f"wrong key: {self._key}")
            return False
        return True

    def check_iterable(self):
        if not self._input.validate():
            return False

        try:
            iter(self._input.value)
            return True
        except TypeError:
            self.trigger_error(error_codes.ERROR_12_DICT_NOT_ITERABLE)
            return False

    @cached_property
    def value(self):
        return self._input.value[self._key]
