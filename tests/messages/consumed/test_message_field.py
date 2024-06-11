import pytest
from tol_lab_share.messages.consumed.message_field import MessageField


class TestMessageField:
    @pytest.mark.parametrize(
        "path, key, name",
        [
            ("", "key", "key"),
            ("path", "key", "path.key"),
            ("root.path", "key", "root.path.key"),
        ],
    )
    def test_generates_name_correctly(self, path, key, name):
        subject = MessageField(path, key, {})
        assert subject.name == name

    def test_extracts_value_correctly(self):
        subject = MessageField("path", "key", {"key": "value"})
        assert subject.value == "value"

    def test_gives_none_value_when_key_missing(self):
        subject = MessageField("path", "key", {})
        assert subject.value is None

    def test_transforms_value_correctly(self):
        subject = MessageField("path", "key", {"key": "value"}, lambda v: v.upper())
        assert subject.value == "VALUE"

    def test_applies_transform_to_missing_value_correctly(self):
        subject = MessageField("path", "key", {}, lambda v: v is None)
        assert subject.value is True

    def test_creates_correct_string_representation(self):
        subject = MessageField("path", "key", {"key": "value"})
        assert str(subject) == "path.key: value"
