from unittest.mock import patch

import pytest
from tests.data.example_bioscan_pool_xp_to_traction_messages import VALID_LIBRARY_PAYLOAD
from tol_lab_share.constants.input_bioscan_pool_xp_to_traction_message import (
    LIBRARY_BOX_BARCODE,
    LIBRARY_CONCENTRATION,
    LIBRARY_INSERT_SIZE,
    LIBRARY_VOLUME,
)
from tol_lab_share.messages.consumed.bioscan_pool_xp_to_traction.library import Library


@pytest.fixture
def subject():
    return Library(VALID_LIBRARY_PAYLOAD, "path", "parent_path")


class TestLibrary:
    def test_init_passes_arguments_to_record(self):
        path = "path"
        parent_path = "parent_path"

        with patch("tol_lab_share.messages.consumed.bioscan_pool_xp_to_traction.library.Record.__init__") as super_init:
            Library(VALID_LIBRARY_PAYLOAD, path, parent_path)

        super_init.assert_called_once_with(VALID_LIBRARY_PAYLOAD, path, parent_path)

    def test_box_barcode_returns_correct_message_field(self, subject):
        with patch(
            "tol_lab_share.messages.consumed.bioscan_pool_xp_to_traction.library.Library._make_field"
        ) as make_field:
            field = subject.box_barcode

        make_field.assert_called_once_with(LIBRARY_BOX_BARCODE)
        assert field == make_field.return_value

    def test_box_barcode_returns_correct_value(self, subject):
        assert subject.box_barcode.value == VALID_LIBRARY_PAYLOAD[LIBRARY_BOX_BARCODE]

    def test_concentration_returns_correct_message_field(self, subject):
        with patch(
            "tol_lab_share.messages.consumed.bioscan_pool_xp_to_traction.library.Library._make_field"
        ) as make_field:
            field = subject.concentration

        make_field.assert_called_once_with(LIBRARY_CONCENTRATION)
        assert field == make_field.return_value

    def test_concentration_returns_correct_value(self, subject):
        assert subject.concentration.value == VALID_LIBRARY_PAYLOAD[LIBRARY_CONCENTRATION]

    def test_insert_size_returns_correct_message_field(self, subject):
        with patch(
            "tol_lab_share.messages.consumed.bioscan_pool_xp_to_traction.library.Library._make_field"
        ) as make_field:
            field = subject.insert_size

        make_field.assert_called_once_with(LIBRARY_INSERT_SIZE)
        assert field == make_field.return_value

    def test_insert_size_returns_correct_value(self, subject):
        assert subject.insert_size.value == VALID_LIBRARY_PAYLOAD[LIBRARY_INSERT_SIZE]

    def test_insert_size_returns_none_when_field_not_present(self, subject):
        subject._payload.pop(LIBRARY_INSERT_SIZE)
        assert subject.insert_size.value is None

    def test_volume_returns_correct_message_field(self, subject):
        with patch(
            "tol_lab_share.messages.consumed.bioscan_pool_xp_to_traction.library.Library._make_field"
        ) as make_field:
            field = subject.volume

        make_field.assert_called_once_with(LIBRARY_VOLUME)
        assert field == make_field.return_value

    def test_volume_returns_correct_value(self, subject):
        assert subject.volume.value == VALID_LIBRARY_PAYLOAD[LIBRARY_VOLUME]
