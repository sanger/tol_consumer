from unittest.mock import MagicMock, call, patch

import pytest

from tol_lab_share.messages.consumed.bioscan_pool_xp_to_traction.validator import Validator


@pytest.fixture
def root_message():
    root = MagicMock()
    root.message_uuid = "uuid1"
    root.request = MagicMock()
    root.request.study_uuid = "uuid2"
    root.sample = MagicMock()
    root.sample.uuid = "uuid3"

    return root


@pytest.fixture(autouse=True)
def mock_check_is_uuid():
    with patch(
        "tol_lab_share.messages.consumed.bioscan_pool_xp_to_traction.validator.BaseValidator._check_is_uuid"
    ) as check_is_uuid:
        yield check_is_uuid


@pytest.fixture
def subject(root_message):
    return Validator(root_message)


def add_error(subject):
    return lambda _: subject._trigger_error(MagicMock())


class TestValidator:
    def test_validate_calls_check_is_uuid(self, subject, mock_check_is_uuid):
        subject.validate()

        mock_check_is_uuid.assert_has_calls([call("uuid1"), call("uuid2"), call("uuid3")])

    def test_validate_returns_true_when_no_errors(self, subject):
        assert subject.validate() is True

    def test_validate_returns_false_when_errors(self, subject, mock_check_is_uuid):
        mock_check_is_uuid.side_effect = add_error(subject)

        assert subject.validate() is False

    def test_validate_logs_correct_error_count(self, subject, mock_check_is_uuid):
        mock_check_is_uuid.side_effect = add_error(subject)

        subject.validate()

        assert len(subject.errors) == 3

    def test_validate_removes_existing_errors_on_validate(self, subject, mock_check_is_uuid):
        mock_check_is_uuid.side_effect = add_error(subject)

        subject._errors = ["error1", "error2", "error3", "error4", "error5"]

        subject.validate()

        assert len(subject.errors) == 3
