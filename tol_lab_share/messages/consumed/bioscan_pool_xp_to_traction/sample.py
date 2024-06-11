from tol_lab_share.constants.input_bioscan_pool_xp_to_traction_message import (
    SAMPLE_SAMPLE_NAME,
    SAMPLE_SAMPLE_UUID,
    SAMPLE_SPECIES_NAME,
)
from tol_lab_share.messages.consumed.message_field import MessageField
from tol_lab_share.messages.consumed.record import Record


class Sample(Record):
    """The sample record of a BioscanPoolXpToTraction message."""

    def __init__(self, payload: dict, path: str, parent_path: str):
        """Initialises the sample record.

        Args:
            payload (dict): The sample payload as a dictionary.
            path (str): The element name to reach this sample record.
            parent_path (str): The path of the parent record.
        """
        super().__init__(payload, path, parent_path)

    @property
    def name(self) -> MessageField:
        """Gets the sample name as a string."""
        return self._make_field(SAMPLE_SAMPLE_NAME)

    @property
    def uuid(self) -> MessageField:
        """Gets the decoded sample UUID as a string."""
        return self._make_field(SAMPLE_SAMPLE_UUID, lambda v: v.decode())

    @property
    def species_name(self) -> MessageField:
        """Gets the species name as a string."""
        return self._make_field(SAMPLE_SPECIES_NAME)
