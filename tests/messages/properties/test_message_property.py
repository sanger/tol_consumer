from tol_lab_share.messages.properties import MessageProperty
from unittest import mock
from tol_lab_share.messages.properties.simple.dict_value import DictValue
from tol_lab_share.messages.properties.simple.value import Value
from tol_lab_share import error_codes
import pytest
from datetime import datetime


class TestMessageProperty:
    def test_can_validate(self):
        instance = MessageProperty(Value("1234"))
        assert instance.validate() is True

        instance = MessageProperty(Value("1234"))
        with mock.patch(
            "tol_lab_share.messages.properties.MessageProperty.validators",
            new_callable=mock.PropertyMock,
        ) as mock_my_property:
            mock_my_property.return_value = [lambda: False]

            assert instance.validate() is False

    def test_can_retrieve_value(self):
        instance = MessageProperty(Value("1234"))
        assert instance.value == "1234"

    def test_check_is_string(self):
        instance = MessageProperty(Value("1234"))
        assert instance.check_is_string() is True

        instance = MessageProperty(Value(b"dd490ee5-fd1d-456d-99fd-eb9d3861e0f9"))
        assert instance.check_is_string() is False

        instance = MessageProperty(Value(""))
        assert instance.check_is_string() is True

        instance = MessageProperty(Value(None))
        assert instance.check_is_string() is False

        instance = MessageProperty(Value(1234))
        assert instance.check_is_string() is False

        instance = MessageProperty(Value({}))
        assert instance.check_is_string() is False

    def test_check_is_integer(self):
        instance = MessageProperty(Value(None))
        assert instance.check_is_integer() is False
        assert len(instance.errors) > 0

        instance = MessageProperty(Value("1234"))
        assert instance.check_is_integer() is False
        assert len(instance.errors) > 0

        instance = MessageProperty(Value([]))
        assert instance.check_is_integer() is False
        assert len(instance.errors) > 0

        instance = MessageProperty(DictValue({"test": 1234}, "wrong!!"))
        assert instance.check_is_integer() is False
        assert len(instance.errors) > 0

        instance = MessageProperty(Value(1234))
        assert instance.check_is_integer() is True
        assert len(instance.errors) == 0

    def test_check_is_date_utc(self):
        instance = MessageProperty(Value("1234"))
        assert instance.check_is_date_utc() is False

        instance = MessageProperty(Value(b"dd490ee5-fd1d-456d-99fd-eb9d3861e0f9"))
        assert instance.check_is_date_utc() is False

        instance = MessageProperty(Value(""))
        assert instance.check_is_date_utc() is False

        instance = MessageProperty(Value(None))
        assert instance.check_is_date_utc() is False

        instance = MessageProperty(Value(datetime.utcnow()))
        assert instance.check_is_date_utc() is True

        instance = MessageProperty(Value({}))
        assert instance.check_is_date_utc() is False

    def test_has_property(self):
        instance = MessageProperty(Value("1234"))
        assert not instance.has_property("test")

        instance.add_property("test", Value("5678"))
        assert instance.has_property("test")

    def test_properties(self):
        instance = MessageProperty(Value("1234"))
        with pytest.raises(KeyError):
            instance.properties("test")

        child_value = Value("5678")
        instance.add_property("test", child_value)
        assert instance.properties("test") == child_value

    def test_can_add_property(self):
        instance = MessageProperty(Value("1234"))

        assert instance.property_name is None
        assert instance.property_source is None

        assert not instance.has_property("test")

        child_value = Value("5678")

        instance.add_property("test", child_value)

        assert child_value.property_name == "test"
        assert child_value.property_source == instance
        assert child_value.property_type == "Property"
        assert child_value.property_position is None

        assert instance.has_property("test")
        assert instance.properties("test") == child_value

    def test_can_add_properties_in_a_list(self):
        instance = MessageProperty(Value("1234"))
        child1 = Value("5678")
        child2 = Value("9012")

        instance.add_property("test", [child1, child2])

        assert child1.property_name == "test[0]"
        assert child1.property_source == instance
        assert child1.property_type == "Array"
        assert child1.property_position == 0

        assert child2.property_name == "test[1]"
        assert child2.property_source == instance
        assert child2.property_type == "Array"
        assert child2.property_position == 1

        assert instance.has_property("test")
        assert instance.properties("test") == [child1, child2]

    def test_trigger_error(self):
        error = error_codes.ERROR_1_UNKNOWN
        instance = MessageProperty(Value("1234"))
        assert len(instance.errors) == 0
        instance.trigger_error(error)
        assert len(instance.errors) == 1
        instance.trigger_error(error.trigger(text="1234"))
        assert len(instance.errors) == 2
        assert instance.errors[1].field == error.field

        instance1 = MessageProperty(Value("1234"))
        instance2 = MessageProperty(Value("1234"))
        instance3 = MessageProperty(Value("1234"))
        instance1.add_property("labware", instance2)
        instance2.add_property("sample", instance3)

        instance1.trigger_error(error)
        instance2.trigger_error(error)
        instance3.trigger_error(error)

        assert instance1.errors[0].field == error.field
        assert instance1.errors[0].origin == error.origin

        assert instance2.errors[0].field == "labware"
        assert instance2.errors[0].origin == error.origin

        assert instance3.errors[0].field == "sample"
        assert instance3.errors[0].origin == "labware"
