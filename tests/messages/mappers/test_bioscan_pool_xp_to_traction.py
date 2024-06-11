from unittest.mock import MagicMock

import pytest

from tol_lab_share.messages.consumed import BioscanPoolXpToTractionMessage
from tol_lab_share.messages.mappers.bioscan_pool_xp_to_traction import BioscanPoolXpToTractionMapper
from tests.data.example_bioscan_pool_xp_to_traction_messages import (
    VALID_BIOSCAN_POOL_XP_TO_TRACTION_PAYLOAD as VALID_PAYLOAD,
)


@pytest.fixture
def bioscan_pool_xp_message():
    return BioscanPoolXpToTractionMessage(VALID_PAYLOAD)


@pytest.fixture
def mock_traction_message():
    mock = MagicMock()
    mock.create_request.return_value = MagicMock()
    return mock


@pytest.fixture
def subject():
    return BioscanPoolXpToTractionMapper()


class TestBioscanPoolXpToTractionMapper:
    def test_map_transfers_values(self, subject, bioscan_pool_xp_message, mock_traction_message):
        subject.map(bioscan_pool_xp_message, mock_traction_message)

        mock_traction_message.create_request.assert_called_once()
        request = mock_traction_message.create_request.return_value

        assert request.container_type == "tubes"
        assert request.container_barcode == bioscan_pool_xp_message.tube_barcode.value

        assert request.library_volume == bioscan_pool_xp_message.library.volume.value
        assert request.library_concentration == bioscan_pool_xp_message.library.concentration.value
        assert request.template_prep_kit_box_barcode == bioscan_pool_xp_message.library.box_barcode.value
        assert request.library_insert_size == bioscan_pool_xp_message.library.insert_size.value

        assert request.cost_code == bioscan_pool_xp_message.request.cost_code.value
        assert request.genome_size == bioscan_pool_xp_message.request.genome_size.value
        assert request.library_type == bioscan_pool_xp_message.request.library_type.value
        assert request.study_uuid == bioscan_pool_xp_message.request.study_uuid.value

        assert request.sample_name == bioscan_pool_xp_message.sample.name.value
        assert request.sample_uuid == bioscan_pool_xp_message.sample.uuid.value
        assert request.species == bioscan_pool_xp_message.sample.species_name.value
