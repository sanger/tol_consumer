from .message_property import MessageProperty
from typing import List, Callable


class AccessionNumber(MessageProperty):
    """MessageProperty subclass to manage parsing of a valid accession number string provided by another
    MessageProperty.
    The accession number to be a string.
    Eg: 'EE1234'
    """

    @property
    def validators(self) -> List[Callable]:
        """Defines the list of validators"""
        return [self.check_is_string]
