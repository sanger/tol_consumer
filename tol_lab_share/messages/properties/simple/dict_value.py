from tol_lab_share.messages.properties import MessageProperty
from functools import cached_property
from tol_lab_share import error_codes
from .value import Value
from typing import Callable, Any


class DictValue(MessageProperty):
    """MessageProperty subclass to manage parsing of the access to the key of a
    dictionary. The input can be a valid dict or another MessageProperty that provides
    as value a valid dict. If the input is not a valid dict, or if the key does not
    exist, it will trigger an error on validation.
    """

    def __init__(self, input: MessageProperty | dict[str, Any], key: str):
        """Constructor that will create an instance to manage the access of the input
        dictionary using the key provided as argument.

        Parameters:
        input (MessageProperty): The dictionary we want to access, wrapped inside another
        MessageProperty class; normally it will be an Input or another DictInput.
        key (str): The key we want to access inside the dictionary provided.

        Returns:
        MessageProperty: instance of MessageProperty
        """
        super().__init__(input)
        if not isinstance(input, MessageProperty):
            self._input = Value(input)
        else:
            self._input = input
        self._key = key

    @property
    def validators(self) -> list[Callable]:
        """Defines the list of validators"""
        return [self.check_has_key]

    def check_has_key(self) -> bool:
        """Function to check that the input has a valid key. If it is not it will
        trigger an error
        Returns:
        bool with the result of the check
        """
        if not self._input.validate():
            return False

        if not self.check_iterable():
            return False

        if self._key not in self._input.value:
            self.trigger_error(error_codes.ERROR_10_DICT_WRONG_KEY, text=f"wrong key: {self._key}")
            return False
        return True

    def check_iterable(self) -> bool:
        """Function to check that the input is a valid dictionary. If it is not iterable it will
        trigger an error
        Returns:
        bool with the result of the check
        """
        try:
            iter(self._input.value)
            return True
        except TypeError:
            self.trigger_error(error_codes.ERROR_12_DICT_NOT_ITERABLE)
            return False

    @cached_property
    def value(self) -> Any:
        """Function that will return the value of the key inside the dictionary.
        Returns:
        Any value stored inside the dict for that key
        """
        return self._input.value[self._key]
