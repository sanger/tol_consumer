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
    mock = MagicMock()
    mock.create_aliquot_message.return_value = MagicMock()
    return mock


@pytest.fixture
def subject():
    return TractionToWarehouseMapper()


class TestTractionToWarehouseMapper:

    def test_map_transfers_values(self, subject, traction_to_warehouse_message, mock_warehouse_message):
        subject.map(traction_to_warehouse_message, mock_warehouse_message)

        mock_warehouse_message.create_aliquot_message.assert_called_once()
        aliquot_message = mock_warehouse_message.create_aliquot_message.return_value

        # Assert the lims
        assert aliquot_message.lims == TRACTION_LIMS

        # Assert the aliquot
        assert aliquot_message.aliquot.id_lims.value == traction_to_warehouse_message.lims_id.value
