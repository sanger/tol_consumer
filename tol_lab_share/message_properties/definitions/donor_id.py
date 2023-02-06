from .message_property import MessageProperty
from typing import List, Callable


class DonorId(MessageProperty):
    """MessageProperty subclass to manage parsing of a valid donor id string provided by another
    MessageProperty.
    The donor id has to be a string.
    Eg: 'donor'
    """

    @property
    def validators(self) -> List[Callable]:
        """Defines the list of validators"""
        return [self.check_is_string]
