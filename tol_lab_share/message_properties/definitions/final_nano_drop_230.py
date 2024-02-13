from .message_property import MessageProperty
from typing import Callable


class FinalNanoDrop230(MessageProperty):
    """MessageProperty subclass to manage parsing of a valid Final NanoDrop 260/230 string provided by another
    MessageProperty.
    The Final NanoDrop 260/230 has to be a string.
    Eg: '260'
    """

    @property
    def validators(self) -> list[Callable]:
        """Defines the list of validators"""
        return [self.check_is_string]
