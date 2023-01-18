from .message_property import MessageProperty
from functools import cached_property
from tol_lab_share import error_codes
import logging
from tol_lab_share.message_properties.input import Input

logger = logging.getLogger(__name__)


class DictInput(MessageProperty):
    def __init__(self, input, key):
        if not isinstance(input, MessageProperty):
            self._input = Input(input)
        else:
            self._input = input
        self._key = key
        self._errors = []
        self._properties = {}

    @property
    def validators(self):
        return [self.check_has_key]

    def check_has_key(self):
        if not self._input.validate():
            self.add_error(error_codes.ERROR_11_PARENT_DICT_WRONG.trigger(instance=self))
            return False

        if not self.check_iterable():
            return False

        if self._key not in self._input.value:
            self.add_error(error_codes.ERROR_10_DICT_WRONG_KEY.trigger(instance=self))
            return False
        return True

    def check_iterable(self):
        if not self._input.validate():
            return False

        try:
            iter(self._input.value)
            return True
        except TypeError:
            self.add_error(error_codes.ERROR_12_DICT_NOT_ITERABLE.trigger(instance=self))
            return False

    @cached_property
    def value(self):
        return self._input.value[self._key]
