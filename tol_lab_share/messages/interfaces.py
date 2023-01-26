from abc import ABC, abstractmethod
from typing import Optional
from tol_lab_share.error_codes import ErrorCode


class OutputFeedbackMessageInterface(ABC):
    @property
    @abstractmethod
    def source_message_uuid(self) -> Optional[bytes]:
        ...

    @source_message_uuid.setter
    @abstractmethod
    def source_message_uuid(self, value: bytes) -> None:
        ...

    @property
    @abstractmethod
    def count_of_total_samples(self) -> Optional[int]:
        ...

    @count_of_total_samples.setter
    @abstractmethod
    def count_of_total_samples(self, value: int) -> None:
        ...

    @property
    @abstractmethod
    def count_of_valid_samples(self) -> Optional[int]:
        ...

    @count_of_valid_samples.setter
    @abstractmethod
    def count_of_valid_samples(self, value: int) -> None:
        ...

    @property
    @abstractmethod
    def operation_was_error_free(self) -> Optional[bool]:
        ...

    @operation_was_error_free.setter
    @abstractmethod
    def operation_was_error_free(self, value: bool) -> None:
        ...

    @abstractmethod
    def to_json(self):
        ...

    @abstractmethod
    def publish(self, publisher, schema_registry, exchange):
        ...

    @abstractmethod
    def add_error(self, error: ErrorCode) -> None:
        ...


class OutputTractionMessageRequestInterface:
    @abstractmethod
    def validate(self) -> bool:
        ...

    @property
    @abstractmethod
    def species(self) -> Optional[str]:
        ...

    @species.setter
    @abstractmethod
    def species(self, value: Optional[str]) -> None:
        ...

    @property
    @abstractmethod
    def container_type(self) -> Optional[str]:
        ...

    @container_type.setter
    @abstractmethod
    def container_type(self, value: Optional[str]) -> None:
        ...

    @property
    @abstractmethod
    def container_location(self) -> Optional[str]:
        ...

    @container_location.setter
    @abstractmethod
    def container_location(self, value: Optional[str]) -> None:
        ...

    @property
    @abstractmethod
    def container_barcode(self) -> Optional[str]:
        ...

    @container_barcode.setter
    @abstractmethod
    def container_barcode(self, value: Optional[str]) -> None:
        ...

    @property
    @abstractmethod
    def sample_uuid(self) -> Optional[str]:
        ...

    @sample_uuid.setter
    @abstractmethod
    def sample_uuid(self, value: Optional[str]) -> None:
        ...

    @property
    @abstractmethod
    def sample_name(self) -> Optional[str]:
        ...

    @sample_name.setter
    @abstractmethod
    def sample_name(self, value: Optional[str]) -> None:
        ...

    @property
    @abstractmethod
    def library_type(self) -> Optional[str]:
        ...

    @library_type.setter
    @abstractmethod
    def library_type(self, value: Optional[str]) -> None:
        ...

    @property
    @abstractmethod
    def study_uuid(self) -> Optional[str]:
        ...

    @study_uuid.setter
    @abstractmethod
    def study_uuid(self, value: Optional[str]) -> None:
        ...


class OutputTractionMessageInterface(ABC):
    @abstractmethod
    def payload(self):
        ...

    @abstractmethod
    def send(self, url):
        ...

    @abstractmethod
    def add_error(self, error: ErrorCode) -> None:
        ...

    @abstractmethod
    def requests(self, position: int) -> OutputTractionMessageRequestInterface:
        ...
