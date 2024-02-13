from .message_property import MessageProperty
from typing import Callable


class PostSPRIVolume(MessageProperty):
    """MessageProperty subclass to manage parsing of a valid Post SPRI Volume (ul) string provided by another
    MessageProperty.
    The Post SPRI Volume (ul) has to be a string.
    Eg: '20'
    """

    @property
    def validators(self) -> list[Callable]:
        """Defines the list of validators"""
        return [self.check_is_string]
