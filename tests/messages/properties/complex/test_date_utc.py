from datetime import datetime

from tol_lab_share.messages.properties.complex import DateUtc
from tol_lab_share.messages.properties.simple import Value


class TestDateUtc:
    def test_validators_behave_correctly(self):
        instance = DateUtc(Value(None))
        assert instance.validate() is False
        assert len(instance.errors) > 0

        instance = DateUtc(Value("1234"))
        assert instance.validate() is False
        assert len(instance.errors) > 0

        instance = DateUtc(Value([]))
        assert instance.validate() is False
        assert len(instance.errors) > 0

        instance = DateUtc(Value(1234))
        assert instance.validate() is False
        assert len(instance.errors) > 0

        instance = DateUtc(Value(datetime(1970, 1, 1, 0, 20, 34, 400000)))
        assert instance.validate() is True
        assert len(instance.errors) == 0

        instance = DateUtc(Value("Testing"))
        assert instance.validate() is False
        assert len(instance.errors) > 0

        instance = DateUtc(Value("United Kingdom"))
        assert instance.validate() is False
        assert len(instance.errors) > 0

    def test_value_is_retrievable(self):
        instance = DateUtc(Value(datetime(1970, 1, 1, 0, 20, 34, 400000)))
        assert instance.value == datetime(1970, 1, 1, 0, 20, 34, 400000)
