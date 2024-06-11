from typing import Callable
from .message_field import MessageField


class Record:
    def __init__(self, payload: dict, name: str = "", parent_path: str = "") -> None:
        super().__init__()
        self._payload = payload
        self._path = name

        if parent_path != "":
            self._path = f"{parent_path}.{name}"

    def _make_field(self, key: str, transform: Callable | None = None) -> MessageField:
        return MessageField(self._path, key, self._payload, transform)
