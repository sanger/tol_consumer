from .message_property import MessageProperty
from typing import List, Callable


class ReasonForPriority(MessageProperty):
    """MessageProperty subclass to manage parsing of a valid Reason for priority required by string provided by another
    MessageProperty.
    The Reason for priority has to be a string.
    Eg: 'reason foes here'
    """

    @property
    def validators(self) -> List[Callable]:
        """Defines the list of validators"""
        return [self.check_is_string]
