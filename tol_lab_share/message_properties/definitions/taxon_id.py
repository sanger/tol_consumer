from .message_property import MessageProperty
from typing import List, Callable


class TaxonId(MessageProperty):
    """MessageProperty subclass to manage parsing of a valid taxon id string provided by another
    MessageProperty.
    The taxon id has to be a string.
    Eg: '9606'
    """

    @property
    def validators(self) -> List[Callable]:
        """Defines the list of validators"""
        return [self.check_is_integer_string]
