from tol_lab_share.constants.input_bioscan_pool_xp_to_traction_message import (
    LIBRARY_BOX_BARCODE,
    LIBRARY_CONCENTRATION,
    LIBRARY_INSERT_SIZE,
    LIBRARY_VOLUME,
)
from tol_lab_share.messages.consumed.message_field import MessageField
from tol_lab_share.messages.consumed.record import Record


class Library(Record):
    """The library record of a BioscanPoolXpToTraction message."""

    def __init__(self, payload: dict, path: str, parent_path: str):
        """Initialises the library record.

        Args:
            payload (dict): The library payload as a dictionary.
            path (str): The element name to reach this library record.
            parent_path (str): The path of the parent record.
        """
        super().__init__(payload, path, parent_path)

    @property
    def box_barcode(self) -> MessageField:
        """Gets the box barcode as a string."""
        return self._make_field(LIBRARY_BOX_BARCODE)

    @property
    def concentration(self) -> MessageField:
        """Gets the concentration as a float."""
        return self._make_field(LIBRARY_CONCENTRATION)

    @property
    def insert_size(self) -> MessageField:
        """Gets the insert size as an integer. The value will be None if the field is not present."""
        return self._make_field(LIBRARY_INSERT_SIZE)

    @property
    def volume(self) -> MessageField:
        """Gets the volume as a float."""
        return self._make_field(LIBRARY_VOLUME)
