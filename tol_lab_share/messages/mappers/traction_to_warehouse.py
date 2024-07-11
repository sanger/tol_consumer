import datetime
import logging

from tol_lab_share.constants.input_traction_volume_tracking_message import TRACTION_LIMS
from tol_lab_share.messages.mlwh.create_aliquot_message import CreateAliquotInWarehouseMessage
from tol_lab_share.messages.consumed import TractionToWarehouseMessage

logger = logging.getLogger(__name__)


class TractionToWarehouseMapper:
    """A mapper for transferring values from TractionVolumeTrackingMessage to CreateAliquotInWarehouseMessage"""

    @staticmethod
    def _map_timestamps(date_value: datetime.datetime) -> "str":
        """Formats datetime timestamps"""
        return date_value.strftime("%Y-%m-%dT%H:%M:%SZ")

    @staticmethod
    def map(
        source: TractionToWarehouseMessage, destination: CreateAliquotInWarehouseMessage
    ) -> CreateAliquotInWarehouseMessage:
        """Maps the warehouse message to a message that's sent to the warehouse through a warehouse

        Args:
            source (TractionWarehouseMessage): The source message from traction
            destination (CreateAliquotInWarehouseMessage): The destination message to warehouse
        """

        # Populate aliquot
        destination.aliquot.id_lims = source.lims_id.value
        destination.aliquot.lims_uuid = source.lims_uuid.value
        destination.aliquot.aliquot_type = source.aliquot_type.value
        destination.aliquot.source_type = source.source_type.value
        destination.aliquot.source_barcode = source.source_barcode.value
        destination.aliquot.sample_name = source.sample_name.value
        destination.aliquot.used_by_type = source.used_by_type.value
        destination.aliquot.used_by_barcode = source.used_by_barcode.value
        destination.aliquot.volume = source.volume.value
        destination.aliquot.concentration = source.concentration.value
        destination.aliquot.insert_size = source.insert_size.value

        # Populating the timestamps
        destination.aliquot.created_at = TractionToWarehouseMapper._map_timestamps(source.create_date_utc.value)
        destination.aliquot.recorded_at = TractionToWarehouseMapper._map_timestamps(source.recorded_at.value)
        destination.aliquot.last_updated = TractionToWarehouseMapper._map_timestamps(source.recorded_at.value)

        # Populate lims
        destination.lims = TRACTION_LIMS

        return destination
