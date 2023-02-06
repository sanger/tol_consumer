from .message_property import MessageProperty
from typing import List, Callable


class PublicName(MessageProperty):
    """MessageProperty subclass to manage parsing of a valid public name string provided by another
    MessageProperty.
    The public name has to be a string.
    Eg: 'public_name_1'
    """

    @property
    def validators(self) -> List[Callable]:
        """Defines the list of validators"""
        return [self.check_is_string]
