from unittest.mock import MagicMock
import pytest

from tol_lab_share.messages.consumed.base_validator import BaseValidator


@pytest.fixture
def subject():
    class SimpleValidator(BaseValidator):
        def validate(self) -> bool:
            return True

    return SimpleValidator()


class TestBaseValidator:
    def test_initialises_successfully(self, subject):
        assert subject is not None

    def test_errors_returns_an_empty_list_before_validation(self, subject):
        assert subject.errors == []

    def test_check_is_uuid_returns_true_when_value_is_a_uuid(self, subject):
        field = MagicMock()
        field.name = "A UUID"
        field.value = "550e8400-e29b-41d4-a716-446655440000"

        assert subject._check_is_uuid(field) is True
        assert len(subject.errors) == 0

    def test_check_is_uuid_returns_false_when_value_is_not_a_uuid(self, subject):
        field = MagicMock()
        field.name = "Not a UUID"
        field.value = "not a uuid"

        assert subject._check_is_uuid(field) is False
        assert len(subject.errors) == 1

    def test_check_is_uuid_adds_error_to_errors_list_when_value_is_not_a_uuid(self, subject):
        field = MagicMock()
        field.name = "Not a UUID"
        field.value = "not a uuid"

        subject._check_is_uuid(field)

        error = subject.errors[0]
        assert error.type_id == 2
        assert error.description == 'Uuid has wrong format, text: "input: not a uuid"'
        assert error.field == "Not a UUID"

    def test_reset_errors_resets_errors_list(self, subject):
        subject._trigger_error(MagicMock())
        assert len(subject.errors) == 1

        subject._reset_errors()
        assert len(subject.errors) == 0

    @pytest.mark.parametrize(
        "text, field",
        [
            ("test error", "test field"),
            (None, "test field"),
            ("test error", None),
        ],
    )
    def test_trigger_error_with_adds_error_to_errors_list(self, subject, text, field):
        mock_error = MagicMock()

        subject._trigger_error(mock_error, text, field)

        assert subject.errors == [mock_error.trigger.return_value]
        assert mock_error.trigger.call_args.kwargs == {"text": text, "field": field}

    def test_trigger_error_uses_default_values_for_text_and_field(self, subject):
        mock_error = MagicMock()

        subject._trigger_error(mock_error)

        assert subject.errors == [mock_error.trigger.return_value]
        assert mock_error.trigger.call_args.kwargs == {"text": None, "field": None}
