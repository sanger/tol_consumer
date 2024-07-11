import datetime

from tol_lab_share.constants.input_traction_volume_tracking_message import TRACTION_LIMS
from tol_lab_share.messages.mlwh.create_aliquot_message import CreateAliquotInWarehouseMessage
from tol_lab_share.messages.consumed import TractionToWarehouseMessage


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
        aliquot_message = destination.create_aliquot_message()

        # Populate aliquot
        aliquot_message.aliquot.id_lims = source.lims_id.value
        aliquot_message.aliquot.lims_uuid = source.lims_uuid.value
        aliquot_message.aliquot.aliquot_type = source.aliquot_type.value
        aliquot_message.aliquot.source_type = source.source_type.value
        aliquot_message.aliquot.source_barcode = source.source_barcode.value
        aliquot_message.aliquot.sample_name = source.sample_name.value
        aliquot_message.aliquot.used_by_type = source.used_by_type.value
        aliquot_message.aliquot.used_by_barcode = source.used_by_barcode.value
        aliquot_message.aliquot.volume = source.volume.value
        aliquot_message.aliquot.concentration = source.concentration.value
        aliquot_message.aliquot.insert_size = source.insert_size.value

        # Populating the timestamps
        aliquot_message.aliquot.created_at = TractionToWarehouseMapper._map_timestamps(source.create_date_utc.value)
        aliquot_message.aliquot.recorded_at = TractionToWarehouseMapper._map_timestamps(source.recorded_at.value)
        aliquot_message.aliquot.last_updated = TractionToWarehouseMapper._map_timestamps(source.recorded_at.value)

        # Populate lims
        aliquot_message.lims = TRACTION_LIMS
        return destination
