from typing import Any, Callable


class MessageField:
    """A wrapper for extracting a field name and value from a record payload."""

    def __init__(self, path: str, key: str, dict: dict[str, Any], transform: Callable | None = None):
        """Initialises the message field.

        Args:
            path (str): The path in the message to reach the field.
            key (str): The key for the field.
            dict (dict[str, Any]): The record payload as a dictionary.
            transform (Callable | None, optional): A transform function for the extracted value.
                Use this to convert the value to a different type or perform mappings.
                Defaults to None (no transformation).
        """
        self._key = key
        self._path = path
        self._dict = dict
        self._transform = transform or (lambda v: v)

    def __str__(self):
        """A string representation of the message field."""
        return f"{self.name}: {self.value}"

    @property
    def name(self) -> str:
        """Gets a descriptive name of the field using the path and the key."""
        if self._path == "":
            return self._key

        return f"{self._path}.{self._key}"

    @property
    def value(self) -> Any:
        """Gets the transformed value of the field."""
        return self._transform(self._dict.get(self._key, None))
