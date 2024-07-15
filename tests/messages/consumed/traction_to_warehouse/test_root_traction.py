from typing import Callable
from unittest.mock import patch

import pytest

from tol_lab_share.constants.input_traction_volume_tracking_message import (
    MESSAGE_UUID,
    CREATED_DATE_UTC,
    LIMS_ID,
    LIMS_UUID,
    ALIQUOT_TYPE,
    SOURCE_TYPE,
    SOURCE_BARCODE,
    SAMPLE_NAME,
    USED_BY_TYPE,
    USED_BY_BARCODE,
    VOLUME,
    CONCENTRATION,
    INSERT_SIZE,
    RECORDED_AT,
)
from tol_lab_share.messages.consumed.traction_to_warehouse.traction_to_mlwh_aliquot import Root
from tests.data.example_create_aliquot_in_mlwh_messages import (
    VALID_TRACTION_TO_WAREHOUSE_MESSAGE as VALID_PAYLOAD,
)


@pytest.fixture
def subject():
    return Root(VALID_PAYLOAD)


class TestRoot:
    def test_init_passes_arguments_to_record(self):
        with patch("tol_lab_share.messages.consumed.traction_to_warehouse.root.Record.__init__") as super_init:
            Root(VALID_PAYLOAD)

        super_init.assert_called_once_with(VALID_PAYLOAD)

    def test_message_uuid_returns_correct_message_field(self, subject, any):
        with patch("tol_lab_share.messages.consumed.traction_to_warehouse.root.Root._make_field") as make_field:
            field = subject.message_uuid

        make_field.assert_called_once_with(MESSAGE_UUID, any(Callable))
        assert field == make_field.return_value

    def test_message_uuid_value_correct(self, subject):
        assert subject.message_uuid.value == VALID_PAYLOAD[MESSAGE_UUID].decode()

    def test_message_create_date_utc_returns_correct_field(self, subject, any):
        with patch("tol_lab_share.messages.consumed.traction_to_warehouse.root.Root._make_field") as make_field:
            field = subject.create_date_utc

        make_field.assert_called_once_with(CREATED_DATE_UTC)
        assert field == make_field.return_value

    def test_create_date_utc_value_correct(self, subject):
        assert subject.create_date_utc.value == VALID_PAYLOAD[CREATED_DATE_UTC]

    def test_lims_id_returns_correct_field(self, subject, any):
        with patch("tol_lab_share.messages.consumed.traction_to_warehouse.root.Root._make_field") as make_field:
            field = subject.lims_id

        make_field.assert_called_once_with(LIMS_ID)
        assert field == make_field.return_value

    def test_lims_id_value_correct(self, subject):
        assert subject.lims_id.value == VALID_PAYLOAD[LIMS_ID]

    def test_lims_uuid_returns_correct_field(self, subject, any):
        with patch("tol_lab_share.messages.consumed.traction_to_warehouse.root.Root._make_field") as make_field:
            field = subject.lims_uuid

        make_field.assert_called_once_with(LIMS_UUID)
        assert field == make_field.return_value

    def test_lims_uuid_value_correct(self, subject):
        assert subject.lims_uuid.value == VALID_PAYLOAD[LIMS_UUID]

    def test_aliquot_type_returns_correct_field(self, subject, any):
        with patch("tol_lab_share.messages.consumed.traction_to_warehouse.root.Root._make_field") as make_field:
            field = subject.aliquot_type

        make_field.assert_called_once_with(ALIQUOT_TYPE)
        assert field == make_field.return_value

    def test_aliquot_type_value_correct(self, subject):
        assert subject.aliquot_type.value == VALID_PAYLOAD[ALIQUOT_TYPE]

    def test_source_type_returns_correct_field(self, subject, any):
        with patch("tol_lab_share.messages.consumed.traction_to_warehouse.root.Root._make_field") as make_field:
            field = subject.source_type

        make_field.assert_called_once_with(SOURCE_TYPE)
        assert field == make_field.return_value

    def test_source_type_value_correct(self, subject):
        assert subject.source_type.value == VALID_PAYLOAD[SOURCE_TYPE]

    def test_source_barcode_returns_correct_field(self, subject, any):
        with patch("tol_lab_share.messages.consumed.traction_to_warehouse.root.Root._make_field") as make_field:
            field = subject.source_barcode

        make_field.assert_called_once_with(SOURCE_BARCODE)
        assert field == make_field.return_value

    def test_source_barcode_value_correct(self, subject):
        assert subject.source_barcode.value == VALID_PAYLOAD[SOURCE_BARCODE]

    def test_sample_name_returns_correct_field(self, subject, any):
        with patch("tol_lab_share.messages.consumed.traction_to_warehouse.root.Root._make_field") as make_field:
            field = subject.sample_name

        make_field.assert_called_once_with(SAMPLE_NAME)
        assert field == make_field.return_value

    def test_sample_name_value_correct(self, subject):
        assert subject.sample_name.value == VALID_PAYLOAD[SAMPLE_NAME]

    def test_used_by_type_returns_correct_field(self, subject, any):
        with patch("tol_lab_share.messages.consumed.traction_to_warehouse.root.Root._make_field") as make_field:
            field = subject.used_by_type

        make_field.assert_called_once_with(USED_BY_TYPE)
        assert field == make_field.return_value

    def test_used_by_type_value_correct(self, subject):
        assert subject.used_by_type.value == VALID_PAYLOAD[USED_BY_TYPE]

    def test_used_by_barcode_returns_correct_field(self, subject, any):
        with patch("tol_lab_share.messages.consumed.traction_to_warehouse.root.Root._make_field") as make_field:
            field = subject.used_by_barcode

        make_field.assert_called_once_with(USED_BY_BARCODE)
        assert field == make_field.return_value

    def test_used_by_barcode_value_correct(self, subject):
        assert subject.used_by_barcode.value == VALID_PAYLOAD[USED_BY_BARCODE]

    def test_volume_returns_correct_field(self, subject, any):
        with patch("tol_lab_share.messages.consumed.traction_to_warehouse.root.Root._make_field") as make_field:
            field = subject.volume

        make_field.assert_called_once_with(VOLUME)
        assert field == make_field.return_value

    def test_volume_value_correct(self, subject):
        assert subject.volume.value == VALID_PAYLOAD[VOLUME]

    def test_concentration_returns_correct_field(self, subject, any):
        with patch("tol_lab_share.messages.consumed.traction_to_warehouse.root.Root._make_field") as make_field:
            field = subject.concentration

        make_field.assert_called_once_with(CONCENTRATION)
        assert field == make_field.return_value

    def test_concentration_value_correct(self, subject):
        assert subject.concentration.value == VALID_PAYLOAD[CONCENTRATION]

    def test_insert_size_returns_correct_field(self, subject, any):
        with patch("tol_lab_share.messages.consumed.traction_to_warehouse.root.Root._make_field") as make_field:
            field = subject.insert_size

        make_field.assert_called_once_with(INSERT_SIZE)
        assert field == make_field.return_value

    def test_insert_size_value_correct(self, subject):
        assert subject.insert_size.value == VALID_PAYLOAD[INSERT_SIZE]

    def test_recorded_at_returns_correct_field(self, subject, any):
        with patch("tol_lab_share.messages.consumed.traction_to_warehouse.root.Root._make_field") as make_field:
            field = subject.recorded_at

        make_field.assert_called_once_with(RECORDED_AT)
        assert field == make_field.return_value

    def test_recorded_at_value_correct(self, subject):
        assert subject.recorded_at.value == VALID_PAYLOAD[RECORDED_AT]
