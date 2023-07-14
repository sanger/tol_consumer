from .message_property import MessageProperty
from typing import List, Callable


class SupplierSampleName(MessageProperty):
    """MessageProperty subclass to manage parsing of a valid supplier sample name string provided by another
    MessageProperty.
    The supplier sample name has to be a string.
    Eg: 'sample_name'
    """

    @property
    def validators(self) -> List[Callable]:
        """Defines the list of validators"""
        return [self.check_is_string]
