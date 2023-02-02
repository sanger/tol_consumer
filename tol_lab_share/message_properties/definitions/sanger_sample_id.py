from .message_property import MessageProperty
from typing import List, Callable


class SangerSampleId(MessageProperty):
    """MessageProperty subclass to manage parsing of a valid sanger sample id string provided by another
    MessageProperty.
    The sanger sample id has to be a string.
    Eg: 'sample_id_1'
    """

    @property
    def validators(self) -> List[Callable]:
        """Defines the list of validators"""
        return [self.check_is_string]
