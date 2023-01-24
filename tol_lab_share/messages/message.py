from typing import List, Optional
from tol_lab_share.error_codes import ErrorCode


class Message:
    def __init__(self):
        self._errors = []

    @property
    def validators(self):
        return []

    @property
    def origin(self):
        return None

    @property
    def field(self):
        return None

    def validate(self):
        return all(list([validator() for validator in self.validators]))

    @property
    def errors(self) -> List[ErrorCode]:
        return self._errors

    def add_error_code(self, error: ErrorCode) -> None:
        self._errors.append(error)

    def trigger_error(self, error_code: ErrorCode, text: Optional[str] = None) -> None:
        self.add_error_code(error_code.trigger(instance=self, origin=self.origin, field=self.field, text=text))
