from abc import ABC, abstractmethod
from typing import Optional
from datetime import datetime
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
    def supplier_name(self) -> Optional[str]:
        ...

    @supplier_name.setter
    @abstractmethod
    def supplier_name(self, value: Optional[str]) -> None:
        ...

    @property
    @abstractmethod
    def date_of_sample_collection(self) -> Optional[datetime]:
        ...

    @date_of_sample_collection.setter
    @abstractmethod
    def date_of_sample_collection(self, value: Optional[datetime]) -> None:
        ...

    @property
    @abstractmethod
    def taxon_id(self) -> Optional[str]:
        ...

    @taxon_id.setter
    @abstractmethod
    def taxon_id(self, value: Optional[str]) -> None:
        ...

    @property
    @abstractmethod
    def accession_number(self) -> Optional[str]:
        ...

    @accession_number.setter
    @abstractmethod
    def accession_number(self, value: Optional[str]) -> None:
        ...

    @property
    @abstractmethod
    def country_of_origin(self) -> Optional[str]:
        ...

    @country_of_origin.setter
    @abstractmethod
    def country_of_origin(self, value: Optional[str]) -> None:
        ...

    @property
    @abstractmethod
    def donor_id(self) -> Optional[str]:
        ...

    @donor_id.setter
    @abstractmethod
    def donor_id(self, value: Optional[str]) -> None:
        ...

    @property
    @abstractmethod
    def sanger_sample_id(self) -> Optional[str]:
        ...

    @sanger_sample_id.setter
    @abstractmethod
    def sanger_sample_id(self, value: Optional[str]) -> None:
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
    def public_name(self) -> Optional[str]:
        ...

    @public_name.setter
    @abstractmethod
    def public_name(self, value: Optional[str]) -> None:
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

    @property
    @abstractmethod
    def cost_code(self) -> Optional[str]:
        ...

    @cost_code.setter
    @abstractmethod
    def cost_code(self, value: Optional[str]) -> None:
        ...

    @property
    @abstractmethod
    def priority_level(self) -> Optional[str]:
        ...

    @priority_level.setter
    @abstractmethod
    def priority_level(self, value: Optional[str]) -> None:
        ...


class TractionQcMessageRequestInterface:
    @abstractmethod
    def validate(self) -> bool:
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
    def sanger_sample_id(self) -> Optional[str]:
        ...

    @sanger_sample_id.setter
    @abstractmethod
    def sanger_sample_id(self, value: Optional[str]) -> None:
        ...

    @property
    @abstractmethod
    def sheared_femto_fragment_size(self) -> Optional[str]:
        ...

    @sheared_femto_fragment_size.setter
    @abstractmethod
    def sheared_femto_fragment_size(self, value: Optional[str]) -> None:
        ...

    @property
    @abstractmethod
    def post_spri_concentration(self) -> Optional[str]:
        ...

    @post_spri_concentration.setter
    @abstractmethod
    def post_spri_concentration(self, value: Optional[str]) -> None:
        ...

    @property
    @abstractmethod
    def post_spri_volume(self) -> Optional[str]:
        ...

    @post_spri_volume.setter
    @abstractmethod
    def post_spri_volume(self, value: Optional[str]) -> None:
        ...

    @property
    @abstractmethod
    def final_nano_drop_280(self) -> Optional[str]:
        ...

    @final_nano_drop_280.setter
    @abstractmethod
    def final_nano_drop_280(self, value: Optional[str]) -> None:
        ...

    @property
    @abstractmethod
    def final_nano_drop_230(self) -> Optional[str]:
        ...

    @final_nano_drop_230.setter
    @abstractmethod
    def final_nano_drop_230(self, value: Optional[str]) -> None:
        ...

    @property
    @abstractmethod
    def final_nano_drop(self) -> Optional[str]:
        ...

    @final_nano_drop.setter
    @abstractmethod
    def final_nano_drop(self, value: Optional[str]) -> None:
        ...

    @property
    @abstractmethod
    def shearing_qc_comments(self) -> Optional[str]:
        ...

    @shearing_qc_comments.setter
    @abstractmethod
    def shearing_qc_comments(self, value: Optional[str]) -> None:
        ...

    @property
    @abstractmethod
    def date_submitted_utc(self) -> Optional[float]:
        ...

    @date_submitted_utc.setter
    @abstractmethod
    def date_submitted_utc(self, value: Optional[float]) -> None:
        ...
