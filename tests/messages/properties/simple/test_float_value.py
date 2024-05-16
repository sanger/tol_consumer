import pytest
from datetime import datetime, UTC
from tol_lab_share.messages.properties.simple import DictValue, FloatValue, Value


class TestFloatValue:
    @pytest.mark.parametrize("test_value", (1234.0, 9876.54321))
    def test_validates_true(self, test_value):
        instance = FloatValue(Value(test_value))
        assert instance.validate() is True
        assert len(instance.errors) == 0

    @pytest.mark.parametrize(
        "test_value",
        ["1234.0", [], {}, b"1234.0", 1234, True, datetime.now(UTC), DictValue({"test": 1234.0}, "wrong!!")],
        ids=[
            "a string",
            "a list",
            "a dictionary",
            "binary data",
            "an integer",
            "a boolean",
            "datetime",
            "an invalid message property",
        ],
    )
    def test_validates_false(self, test_value):
        instance = FloatValue(Value(test_value))
        assert instance.validate() is False
        assert len(instance.errors) > 0
