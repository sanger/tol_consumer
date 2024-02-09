from .message_property import MessageProperty
from typing import Callable


class ShearingAndQCComments(MessageProperty):
    """MessageProperty subclass to manage parsing of a valid Shearing & QC comments string provided by another
    MessageProperty.
    The Shearing & QC comments has to be a string.
    Eg: 'comments'
    """

    @property
    def validators(self) -> list[Callable]:
        """Defines the list of validators"""
        return [self.check_is_string]
