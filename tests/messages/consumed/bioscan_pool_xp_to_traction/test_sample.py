from typing import Callable
from unittest.mock import patch

import pytest
from tests.data.example_bioscan_pool_xp_to_traction_messages import VALID_SAMPLE_PAYLOAD
from tol_lab_share.constants.input_bioscan_pool_xp_to_traction_message import (
    SAMPLE_SAMPLE_NAME,
    SAMPLE_SAMPLE_UUID,
    SAMPLE_SPECIES_NAME,
)
from tol_lab_share.messages.consumed.bioscan_pool_xp_to_traction.sample import Sample


@pytest.fixture
def subject():
    return Sample(VALID_SAMPLE_PAYLOAD.copy(), "path", "parent_path")


class TestSample:
    def test_init_passes_arguments_to_record(self):
        path = "path"
        parent_path = "parent_path"

        with patch("tol_lab_share.messages.consumed.bioscan_pool_xp_to_traction.sample.Record.__init__") as super_init:
            Sample(VALID_SAMPLE_PAYLOAD, path, parent_path)

        super_init.assert_called_once_with(VALID_SAMPLE_PAYLOAD, path, parent_path)

    def test_name_returns_correct_message_field(self, subject):
        with patch(
            "tol_lab_share.messages.consumed.bioscan_pool_xp_to_traction.sample.Sample._make_field"
        ) as make_field:
            field = subject.name

        make_field.assert_called_once_with(SAMPLE_SAMPLE_NAME)
        assert field == make_field.return_value

    def test_name_returns_correct_value(self, subject):
        assert subject.name.value == VALID_SAMPLE_PAYLOAD[SAMPLE_SAMPLE_NAME]

    def test_uuid_returns_correct_message_field(self, subject, any):
        with patch(
            "tol_lab_share.messages.consumed.bioscan_pool_xp_to_traction.sample.Sample._make_field"
        ) as make_field:
            field = subject.uuid

        make_field.assert_called_once_with(SAMPLE_SAMPLE_UUID, any(Callable))
        assert field == make_field.return_value

    def test_uuid_returns_correct_value(self, subject):
        assert subject.uuid.value == VALID_SAMPLE_PAYLOAD[SAMPLE_SAMPLE_UUID].decode()

    def test_species_name_returns_correct_message_field(self, subject):
        with patch(
            "tol_lab_share.messages.consumed.bioscan_pool_xp_to_traction.sample.Sample._make_field"
        ) as make_field:
            field = subject.species_name

        make_field.assert_called_once_with(SAMPLE_SPECIES_NAME)
        assert field == make_field.return_value

    def test_species_name_returns_correct_value(self, subject):
        assert subject.species_name.value == VALID_SAMPLE_PAYLOAD[SAMPLE_SPECIES_NAME]
