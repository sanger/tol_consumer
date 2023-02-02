from .message_property import MessageProperty
from typing import List, Callable


class CommonName(MessageProperty):
    """MessageProperty subclass to manage parsing of a valid common name string provided by another
    MessageProperty.
    The common name has to be a string.
    Eg: 'test'
    """

    @property
    def validators(self) -> List[Callable]:
        """Defines the list of validators"""
        return [self.check_is_string]
