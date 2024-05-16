import pytest
from tol_lab_share.messages.properties.simple.string_value import StringValue
from tol_lab_share.messages.properties.simple.value import Value


class TestStringValue:
    @pytest.mark.parametrize(
        "test_value, optional, should_be_valid",
        [
            (None, False, False),
            (None, True, True),
            (1234, False, False),
            (1234, True, False),
            ([], False, False),
            ([], True, False),
            ("1234", False, True),
            ("1234", True, True),
        ],
    )
    def test_validates_strings(self, test_value, optional, should_be_valid):
        instance = StringValue(Value(test_value), optional=optional)
        assert instance.validate() is should_be_valid
        if should_be_valid:
            assert len(instance.errors) == 0
        else:
            assert len(instance.errors) > 0
