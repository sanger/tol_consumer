from abc import ABC, abstractmethod
from functools import cached_property
from typing import Any, Optional

from tol_lab_share.messages.interfaces import (
    OutputFeedbackMessageInterface,
    OutputTractionMessageInterface,
    TractionQcMessageInterface,
)


class MessagePropertyInterface(ABC):
    @abstractmethod
    def validate(self):
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
    def add_to_feedback_message(self, feedback_message: OutputFeedbackMessageInterface) -> None:
        ...

    @abstractmethod
    def add_to_traction_message(self, traction_message: OutputTractionMessageInterface) -> None:
        ...

    @abstractmethod
    def add_to_traction_qc_message(self, traction_qc_message: TractionQcMessageInterface) -> None:
        ...

    @property
    @abstractmethod
    def property_name(self) -> Optional[str]:
        ...

    @property_name.setter
    @abstractmethod
    def property_name(self, value: str) -> None:
        ...

    @property
    @abstractmethod
    def property_source(self) -> Optional[Any]:
        ...

    @property_source.setter
    @abstractmethod
    def property_source(self, value: Any) -> None:
        ...

    @property
    @abstractmethod
    def property_position(self) -> Optional[int]:
        ...

    @property_position.setter
    @abstractmethod
    def property_position(self, value: Any) -> None:
        ...

    @property
    @abstractmethod
    def property_type(self) -> Optional[str]:
        ...

    @property_type.setter
    @abstractmethod
    def property_type(self, value: Any) -> None:
        ...
