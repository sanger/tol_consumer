from typing import List
from tol_lab_share.error_codes import ErrorCode


class Message:
    def __init__(self):
        self._errors = []

    @property
    def validators(self):
        return []

    def validate(self):
        self._errors = []
        return all(list([validator() for validator in self.validators]))

    @property
    def errors(self) -> List[ErrorCode]:
        return self._errors

    def add_error_code(self, error: ErrorCode) -> None:
        self._errors.append(error)
