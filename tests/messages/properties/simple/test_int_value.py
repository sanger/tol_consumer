import pytest
from datetime import datetime, UTC
from tol_lab_share.messages.properties.simple import DictValue, IntValue, Value


class TestIntValue:
    @pytest.mark.parametrize(
        "test_value",
        (1234, 9876),
    )
    @pytest.mark.parametrize("optional", (True, False), ids=["optional", "not optional"])
    def test_validates_true(self, test_value, optional):
        instance = IntValue(Value(test_value), optional=optional)
        assert instance.validate() is True
        assert len(instance.errors) == 0

    @pytest.mark.parametrize(
        "test_value",
        ["1234", [], {}, b"1234", 1234.0, datetime.now(UTC), DictValue({"test": 1234}, "wrong!!")],
        ids=["a string", "a list", "a dictionary", "binary data", "a float", "datetime", "an invalid message property"],
    )
    @pytest.mark.parametrize("optional", (True, False), ids=["optional", "not optional"])
    def test_validates_false(self, test_value, optional):
        instance = IntValue(Value(test_value), optional=optional)
        assert instance.validate() is False
        assert len(instance.errors) > 0

    def test_validates_true_for_none_when_optional(self):
        instance = IntValue(Value(None), optional=True)
        assert instance.validate() is True
        assert len(instance.errors) == 0

    def test_validates_false_for_none_when_not_optional(self):
        instance = IntValue(Value(None), optional=False)
        assert instance.validate() is False
        assert len(instance.errors) > 0

    def test_validates_false_for_none_with_default_optional_flag(self):
        instance = IntValue(Value(None))
        assert instance.validate() is False
        assert len(instance.errors) > 0
