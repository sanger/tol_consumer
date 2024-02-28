from ...messages.properties.message_property import MessageProperty
from typing import Callable


class CostCode(MessageProperty):
    """MessageProperty subclass to manage parsing of a valid cost_code string provided by another
    MessageProperty.
    The cost code has to be a string.
    Eg: 'S1234'
    """

    @property
    def validators(self) -> list[Callable]:
        """Defines the list of validators"""
        return [self.check_is_string]
