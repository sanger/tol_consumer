from tol_lab_share.constants.input_bioscan_pool_xp_to_traction_message import (
    REQUEST_COST_CODE,
    REQUEST_GENOME_SIZE,
    REQUEST_LIBRARY_TYPE,
    REQUEST_STUDY_UUID,
)
from tol_lab_share.messages.consumed.message_field import MessageField
from tol_lab_share.messages.consumed.record import Record


class Request(Record):
    """The request record of a BioscanPoolXpToTraction message."""

    def __init__(self, payload: dict, path: str, parent_path: str):
        """Initialises the request record.

        Args:
            payload (dict): The request payload as a dictionary.
            path (str): The element name to reach this request record.
            parent_path (str): The path of the parent record.
        """
        super().__init__(payload, path, parent_path)

    @property
    def cost_code(self) -> MessageField:
        """Gets the cost code as a string."""
        return self._make_field(REQUEST_COST_CODE)

    @property
    def genome_size(self) -> MessageField:
        """Gets the genome size as a string. The value will be None if the field is not present."""
        return self._make_field(REQUEST_GENOME_SIZE)

    @property
    def library_type(self) -> MessageField:
        """Gets the library type as a string."""
        return self._make_field(REQUEST_LIBRARY_TYPE)

    @property
    def study_uuid(self) -> MessageField:
        """Gets the decoded study UUID as a string."""
        return self._make_field(REQUEST_STUDY_UUID, lambda v: v.decode())
