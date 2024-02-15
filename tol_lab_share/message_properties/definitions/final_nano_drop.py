from .message_property import MessageProperty
from typing import Callable


class FinalNanoDrop(MessageProperty):
    """MessageProperty subclass to manage parsing of a valid Final NanoDrop string provided by another
    MessageProperty.
    The Final NanoDrop has to be a string.
    Eg: '100'
    """

    @property
    def validators(self) -> list[Callable]:
        """Defines the list of validators"""
        return [self.check_is_string]
