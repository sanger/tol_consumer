import pytest
from datetime import datetime, UTC
from tol_lab_share.messages.properties.simple import DictValue, BooleanValue, Value


class TestBooleanValue:
    @pytest.mark.parametrize("test_value", (True, False))
    def test_validates_true(self, test_value):
        instance = BooleanValue(Value(test_value))
        assert instance.validate() is True
        assert len(instance.errors) == 0

    @pytest.mark.parametrize(
        "test_value",
        ["True", [], {}, b"True", 1, 1.0, datetime.now(UTC), DictValue({"test": True}, "wrong!!")],
        ids=[
            "a string",
            "a list",
            "a dictionary",
            "binary data",
            "an integer",
            "a float",
            "datetime",
            "an invalid message property",
        ],
    )
    def test_validates_false(self, test_value):
        instance = BooleanValue(Value(test_value))
        assert instance.validate() is False
        assert len(instance.errors) > 0
