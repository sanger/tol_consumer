from tol_lab_share.messages.output_feedback_message import OutputFeedbackMessage
from typing import Optional, Any
from functools import cached_property
from abc import ABC, abstractmethod


class DataResolverInterface(ABC):
    @abstractmethod
    def validate(self):
        ...

    @abstractmethod
    def resolve(self):
        ...

    @property
    @abstractmethod
    def errors(self) -> Any:
        ...

    @cached_property
    @abstractmethod
    def value(self) -> Optional[Any]:
        ...

    @abstractmethod
    def add_to_feedback_message(self, feedback_message: OutputFeedbackMessage) -> None:
        ...
