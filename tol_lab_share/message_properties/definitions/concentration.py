from ...messages.properties.message_property import MessageProperty
from typing import Callable


class Concentration(MessageProperty):
    """MessageProperty subclass to manage parsing of a valid concentration provided by another
    MessageProperty. The concentration has to be a valid float string.
    Eg: '1.23'
    """

    @property
    def validators(self) -> list[Callable]:
        """Defines the list of validators"""
        return [self.check_is_string]
