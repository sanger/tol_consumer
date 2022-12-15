from typing import List, Optional


class OutputFeedbackMessage:
    def __init__(self):
        self._source_message_uuid : Optional[str] = None
        self._count_of_total_samples : Optional[int] = None
        self._count_of_valid_samples = None
        self._operation_was_error_free = None
        self._errors = []

    @property
    def source_message_uuid(self) -> str:
        return self._source_message_uuid

    @property
    def count_of_total_samples(self) -> int:
        return self._count_of_total_samples

    @property
    def count_of_valid_samples(self) -> int:
        return self._count_of_valid_samples

    @property
    def operation_was_error_free(self) -> int:
        return self._operation_was_error_free

    @property
    def errors(self) -> List[List[str]]:
        return self._errors

    def add_error(self, type_id, origin, sample_uuid, field, description):
        self._errors.append([type_id, origin, sample_uuid, field, description])

    @source_message_uuid.setter
    def source_message_uuid(self, value: str) -> None:
        self._source_message_uuid = value

    @count_of_total_samples.setter
    def count_of_total_samples(self, value: int) -> None:
        self._count_of_total_samples = value

    @count_of_valid_samples.setter
    def count_of_valid_samples(self, value: int) -> None:
        self._count_of_valid_samples = value

    @operation_was_error_free.setter
    def operation_was_error_free(self, value: int) -> None:
        self._operation_was_error_free = value
