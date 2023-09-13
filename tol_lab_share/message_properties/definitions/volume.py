from .message_property import MessageProperty
from typing import List, Callable


class Volume(MessageProperty):
    """MessageProperty subclass to manage parsing of a valid volume provided by another
    MessageProperty.
    The volume has to be a float string.
    Eg: '43.335'
    """

    @property
    def validators(self) -> List[Callable]:
        """Defines the list of validators"""
        return [self.check_is_string]
