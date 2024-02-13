from .message_property import MessageProperty
from typing import Callable


class PostSPRIConcentration(MessageProperty):
    """MessageProperty subclass to manage parsing of a valid Post SPRI Concentration (ng/ul) string provided by another
    MessageProperty.
    The Post SPRI Concentration (ng/ul) has to be a string.
    Eg: '10'
    """

    @property
    def validators(self) -> list[Callable]:
        """Defines the list of validators"""
        return [self.check_is_string]
