from typing import Any
from unittest.mock import patch
import pytest
from tol_lab_share.messages.consumed.record import Record


@pytest.fixture
def transform():
    def decode_transform(v):
        v.decode()

    return decode_transform


@pytest.fixture
def payload() -> dict[str, Any]:
    return {}


class TestRecord:
    @pytest.mark.parametrize(
        "payload, name, parent_path",
        [
            ({}, "", ""),
            ({}, "", "root"),
            ({}, "name", ""),
            ({}, "name", "root"),
        ],
    )
    def test_initialises_successfully_with_all_parameters(self, payload, name, parent_path):
        record = Record(payload, name, parent_path)
        assert record is not None

    def test_initialises_successfully_with_no_name(self):
        record = Record({}, parent_path="parent_path")
        assert record is not None

    def test_initialises_successfully_with_no_parent_path(self):
        record = Record({}, name="name")
        assert record is not None

    def test_initialises_successfully_with_no_optional_parameters(self):
        record = Record({})
        assert record is not None

    @pytest.mark.parametrize(
        "name, parent_path, expected_path",
        [
            ("", "", ""),
            ("", "root", "root."),
            ("name", "", "name"),
            ("name", "root", "root.name"),
        ],
    )
    def test_make_field_with_only_a_key_creates_the_correct_message_field(
        self, name, parent_path, expected_path, payload
    ):
        record = Record(payload, name, parent_path)

        with patch("tol_lab_share.messages.consumed.record.MessageField") as mock_message_field:
            record._make_field("key")
            mock_message_field.assert_called_with(expected_path, "key", payload, None)

    @pytest.mark.parametrize(
        "name, parent_path, expected_path",
        [
            ("", "", ""),
            ("", "root", "root."),
            ("name", "", "name"),
            ("name", "root", "root.name"),
        ],
    )
    def test_make_field_with_a_transform_creates_the_correct_message_field(
        self, name, parent_path, expected_path, transform, payload
    ):
        record = Record(payload, name, parent_path)

        with patch("tol_lab_share.messages.consumed.record.MessageField") as mock_message_field:
            record._make_field("key", transform)
            mock_message_field.assert_called_with(expected_path, "key", payload, transform)
