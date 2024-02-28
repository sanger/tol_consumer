from ...messages.properties.message_property import MessageProperty
from typing import Callable


class GenomeSize(MessageProperty):
    """MessageProperty subclass to manage parsing of a valid genome size string provided by another
    MessageProperty.
    The genome size has to be a string.
    Eg: '25'
    """

    @property
    def validators(self) -> list[Callable]:
        """Defines the list of validators"""
        return [self.check_is_string]
