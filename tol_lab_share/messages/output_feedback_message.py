from typing import List, Optional


class OutputFeedbackMessage:
    def __init__(self):
        self._source_message_uuid: Optional[bytes] = None
        self._count_of_total_samples: Optional[int] = None
        self._count_of_valid_samples: Optional[int] = None
        self._operation_was_error_free: Optional[bool] = None
        self._errors: List[List[str]] = []

    @property
    def source_message_uuid(self) -> Optional[bytes]:
        return self._source_message_uuid

    @source_message_uuid.setter
    def source_message_uuid(self, value: bytes) -> None:
        self._source_message_uuid = value

    @property
    def count_of_total_samples(self) -> Optional[int]:
        return self._count_of_total_samples

    @count_of_total_samples.setter
    def count_of_total_samples(self, value: int) -> None:
        self._count_of_total_samples = value

    @property
    def count_of_valid_samples(self) -> Optional[int]:
        return self._count_of_valid_samples

    @count_of_valid_samples.setter
    def count_of_valid_samples(self, value: int) -> None:
        self._count_of_valid_samples = value

    @property
    def operation_was_error_free(self) -> Optional[bool]:
        return self._operation_was_error_free

    @operation_was_error_free.setter
    def operation_was_error_free(self, value: bool) -> None:
        self._operation_was_error_free = value

    @property
    def errors(self) -> List[List[str]]:
        return self._errors

    def add_error(self, type_id, origin, sample_uuid, field, description):
        self._errors.append([type_id, origin, sample_uuid, field, description])

    def add_error_code(self, error_code, sample_uuid=None):
        self._errors.append(
            [error_code.type_id, error_code.origin, sample_uuid, error_code.field, error_code.description]
        )
