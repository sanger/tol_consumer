from tol_lab_share.constants.input_traction_volume_tracking_message import (
    MESSAGE_UUID,
    CREATED_DATE_UTC,
    ALIQUOT_UUID,
    ALIQUOT_TYPE,
    SOURCE_TYPE,
    SOURCE_BARCODE,
    SAMPLE_NAME,
    USED_BY_TYPE,
    USED_BY_BARCODE,
    CONCENTRATION,
    INSERT_SIZE,
    RECORDED_AT,
    LIMS_ID,
    VOLUME,
)
from tol_lab_share.messages.consumed import MessageField
from tol_lab_share.messages.consumed.record import Record


class TractionToMlwhAliquot(Record):
    """
    The root record of TractionVolumeTrackingMessage message.
    This forms the message coming from traction to the message queue.
    """

    def __init__(self, payload: dict):
        """Initialises the root record

        Args:
            payload (dict): The root message payload as a dictionary
        """
        super().__init__(payload)

    @property
    def message_uuid(self) -> MessageField:
        """Gets the decoded message UUID as a string."""
        return self._make_field(MESSAGE_UUID, lambda v: v.decode())

    @property
    def create_date_utc(self) -> MessageField:
        """Gets the UTC creation date of the message as a datetime object."""
        return self._make_field(CREATED_DATE_UTC)

    @property
    def lims_id(self) -> MessageField:
        """Gets the UTC creation date of the message as a datetime object."""
        return self._make_field(LIMS_ID)

    @property
    def aliquot_uuid(self) -> MessageField:
        """Gets the UUID of the aliquot in the LIMS system as a string."""
        return self._make_field(ALIQUOT_UUID)

    @property
    def aliquot_type(self) -> MessageField:
        """Gets the aliquot type as a string."""
        return self._make_field(ALIQUOT_TYPE)

    @property
    def source_type(self) -> MessageField:
        """Gets source type as a string."""
        return self._make_field(SOURCE_TYPE)

    @property
    def source_barcode(self) -> MessageField:
        """Gets the source barcode as a string."""
        return self._make_field(SOURCE_BARCODE)

    @property
    def sample_name(self) -> MessageField:
        """Gets the sample name as a string."""
        return self._make_field(SAMPLE_NAME)

    @property
    def used_by_type(self) -> MessageField:
        """Gets the used by type as a string."""
        return self._make_field(USED_BY_TYPE)

    @property
    def used_by_barcode(self) -> MessageField:
        """Gets used by barcode as a string."""
        return self._make_field(USED_BY_BARCODE)

    @property
    def volume(self) -> MessageField:
        """Gets the concentration as a float."""
        return self._make_field(VOLUME)

    @property
    def concentration(self) -> MessageField:
        """Gets the concentration as a float."""
        return self._make_field(CONCENTRATION)

    @property
    def insert_size(self) -> MessageField:
        """Gets the insert size as an integer."""
        return self._make_field(INSERT_SIZE)

    @property
    def recorded_at(self) -> MessageField:
        """Gets the recorded at as a datetime object."""
        return self._make_field(RECORDED_AT)
