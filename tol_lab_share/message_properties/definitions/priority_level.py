from typing import Callable

from .message_property import MessageProperty


class PriorityLevel(MessageProperty):
    """MessageProperty subclass to manage parsing of a valid Priority level (if High or Medium)
    string provided by another
    MessageProperty.
    The Priority level (if High or Medium) has to be a string.
    Eg: 'Medium'
    """

    @property
    def validators(self) -> list[Callable]:
        """Defines the list of validators"""
        return [self.check_is_string]
