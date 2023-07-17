from .message_property import MessageProperty
from typing import List, Callable


class DateRequiredBy(MessageProperty):
    """MessageProperty subclass to manage parsing of a valid Date data required by string provided by another
    MessageProperty.
    The Date data required by has to be a string.
    Eg: 'Long read'
    """

    @property
    def validators(self) -> List[Callable]:
        """Defines the list of validators"""
        return [self.check_is_string]
