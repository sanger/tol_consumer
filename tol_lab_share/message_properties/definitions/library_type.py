from .message_property import MessageProperty
from typing import Callable


class LibraryType(MessageProperty):
    """MessageProperty subclass to manage parsing of a valid library type string provided by another
    MessageProperty.
    The library type has to be a string.
    Eg: 'library1'
    """

    @property
    def validators(self) -> list[Callable]:
        """Defines the list of validators"""
        return [self.check_is_string]
