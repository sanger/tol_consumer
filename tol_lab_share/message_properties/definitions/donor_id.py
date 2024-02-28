from ...messages.properties.message_property import MessageProperty
from typing import Callable


class DonorId(MessageProperty):
    """MessageProperty subclass to manage parsing of a valid donor id string provided by another
    MessageProperty.
    The donor id has to be a string.
    Eg: 'donor'
    """

    @property
    def validators(self) -> list[Callable]:
        """Defines the list of validators"""
        return [self.check_is_string]
