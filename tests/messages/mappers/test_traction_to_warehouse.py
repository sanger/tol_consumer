from unittest.mock import MagicMock

import pytest

from tol_lab_share.constants.input_traction_volume_tracking_message import TRACTION_LIMS
from tol_lab_share.messages.consumed import TractionToWarehouseMessage
from tests.data.example_create_aliquot_in_mlwh_messages import (
    VALID_TRACTION_TO_WAREHOUSE_MESSAGE as VALID_PAYLOAD,
)
from tol_lab_share.messages.mappers.traction_to_warehouse import TractionToWarehouseMapper


@pytest.fixture
def traction_to_warehouse_message():
    return TractionToWarehouseMessage(VALID_PAYLOAD)


@pytest.fixture
def mock_warehouse_message():
    return MagicMock()


@pytest.fixture
def subject():
    return TractionToWarehouseMapper()


class TestTractionToWarehouseMapper:

    def test_map_transfers_values(self, subject, traction_to_warehouse_message, mock_warehouse_message):
        subject.map(traction_to_warehouse_message, mock_warehouse_message)

        # Assert the lims
        assert mock_warehouse_message.lims == TRACTION_LIMS

        # Assert the aliquot
        assert mock_warehouse_message.aliquot.id_lims == traction_to_warehouse_message.lims_id.value
        assert mock_warehouse_message.aliquot.lims_uuid == traction_to_warehouse_message.lims_uuid.value
        assert mock_warehouse_message.aliquot.aliquot_type == traction_to_warehouse_message.aliquot_type.value
        assert mock_warehouse_message.aliquot.source_type == traction_to_warehouse_message.source_type.value
        assert mock_warehouse_message.aliquot.source_barcode == traction_to_warehouse_message.source_barcode.value
        assert mock_warehouse_message.aliquot.sample_name == traction_to_warehouse_message.sample_name.value
        assert mock_warehouse_message.aliquot.used_by_type == traction_to_warehouse_message.used_by_type.value
        assert mock_warehouse_message.aliquot.used_by_barcode == traction_to_warehouse_message.used_by_barcode.value
        assert mock_warehouse_message.aliquot.volume == traction_to_warehouse_message.volume.value
        assert mock_warehouse_message.aliquot.concentration == traction_to_warehouse_message.concentration.value
        assert mock_warehouse_message.aliquot.insert_size == traction_to_warehouse_message.insert_size.value
        assert (
            mock_warehouse_message.aliquot.created_at
            == traction_to_warehouse_message.create_date_utc.value.strftime("%Y-%m-%dT%H:%M:%SZ")
        )
        assert mock_warehouse_message.aliquot.created_at == traction_to_warehouse_message.recorded_at.value.strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        )
        assert mock_warehouse_message.aliquot.last_updated == traction_to_warehouse_message.recorded_at.value.strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        )
