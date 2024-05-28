from typing import Callable
from unittest.mock import patch

import pytest
from tests.data.example_bioscan_pool_xp_to_traction_messages import VALID_REQUEST_PAYLOAD
from tol_lab_share.constants.input_bioscan_pool_xp_to_traction_message import (
    REQUEST_COST_CODE,
    REQUEST_GENOME_SIZE,
    REQUEST_LIBRARY_TYPE,
    REQUEST_STUDY_UUID,
)
from tol_lab_share.messages.consumed.bioscan_pool_xp_to_traction.request import Request


@pytest.fixture
def subject():
    return Request(VALID_REQUEST_PAYLOAD.copy(), "path", "parent_path")


class TestRequest:
    def test_init_passes_arguments_to_record(self):
        path = "path"
        parent_path = "parent_path"

        with patch("tol_lab_share.messages.consumed.bioscan_pool_xp_to_traction.request.Record.__init__") as super_init:
            Request(VALID_REQUEST_PAYLOAD, path, parent_path)

        super_init.assert_called_once_with(VALID_REQUEST_PAYLOAD, path, parent_path)

    def test_cost_code_returns_correct_message_field(self, subject):
        with patch(
            "tol_lab_share.messages.consumed.bioscan_pool_xp_to_traction.request.Request._make_field"
        ) as make_field:
            field = subject.cost_code

        make_field.assert_called_once_with(REQUEST_COST_CODE)
        assert field == make_field.return_value

    def test_cost_code_returns_correct_value(self, subject):
        assert subject.cost_code.value == VALID_REQUEST_PAYLOAD[REQUEST_COST_CODE]

    def test_genome_size_returns_correct_message_field(self, subject):
        with patch(
            "tol_lab_share.messages.consumed.bioscan_pool_xp_to_traction.request.Request._make_field"
        ) as make_field:
            field = subject.genome_size

        make_field.assert_called_once_with(REQUEST_GENOME_SIZE)
        assert field == make_field.return_value

    def test_genome_size_returns_correct_value(self, subject):
        assert subject.genome_size.value == VALID_REQUEST_PAYLOAD[REQUEST_GENOME_SIZE]

    def test_genome_size_returns_none_when_not_present(self, subject):
        subject._payload.pop(REQUEST_GENOME_SIZE)
        assert subject.genome_size.value is None

    def test_library_type_returns_correct_message_field(self, subject):
        with patch(
            "tol_lab_share.messages.consumed.bioscan_pool_xp_to_traction.request.Request._make_field"
        ) as make_field:
            field = subject.library_type

        make_field.assert_called_once_with(REQUEST_LIBRARY_TYPE)
        assert field == make_field.return_value

    def test_library_type_returns_correct_value(self, subject):
        assert subject.library_type.value == VALID_REQUEST_PAYLOAD[REQUEST_LIBRARY_TYPE]

    def test_study_uuid_returns_correct_message_field(self, subject, any):
        with patch(
            "tol_lab_share.messages.consumed.bioscan_pool_xp_to_traction.request.Request._make_field"
        ) as make_field:
            field = subject.study_uuid

        make_field.assert_called_once_with(REQUEST_STUDY_UUID, any(Callable))
        assert field == make_field.return_value

    def test_study_uuid_returns_correct_value(self, subject):
        assert subject.study_uuid.value == VALID_REQUEST_PAYLOAD[REQUEST_STUDY_UUID].decode()
