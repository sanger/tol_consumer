from tol_lab_share.messages.properties import MessageProperty
from unittest import mock
from tol_lab_share.messages.properties.value_wrappers import DictValue, Value
from tol_lab_share import error_codes
import pytest
from datetime import datetime


def test_message_property_can_initialize():
    instance = MessageProperty(Value("1234"))
    assert instance is not None


def test_message_property_can_validate():
    instance = MessageProperty(Value("1234"))
    assert instance.validate() is True

    instance = MessageProperty(Value("1234"))
    with mock.patch(
        "tol_lab_share.messages.properties.MessageProperty.validators",
        new_callable=mock.PropertyMock,
    ) as mock_my_property:
        mock_my_property.return_value = [lambda: False]

        assert instance.validate() is False


def test_message_property_can_get_value():
    instance = MessageProperty(Value("1234"))
    assert instance.value == "1234"


def test_message_property_check_is_string():
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


def test_message_property_check_is_integer():
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


def test_message_property_check_is_integer_string():
    instance = MessageProperty(Value(None))
    assert instance.check_is_integer_string() is False
    assert len(instance.errors) > 0

    instance = MessageProperty(Value("1234"))
    assert instance.check_is_integer_string() is True
    assert len(instance.errors) == 0

    instance = MessageProperty(Value([]))
    assert instance.check_is_integer_string() is False
    assert len(instance.errors) > 0

    instance = MessageProperty(Value(1234))
    assert instance.check_is_integer_string() is False
    assert len(instance.errors) > 0

    instance = MessageProperty(Value("1234.0"))
    assert instance.check_is_integer_string() is False
    assert len(instance.errors) > 0

    instance = MessageProperty(Value("abcd"))
    assert instance.check_is_integer_string() is False
    assert len(instance.errors) > 0


def test_message_property_check_is_float():
    instance = MessageProperty(Value(None))
    assert instance.check_is_float() is False
    assert len(instance.errors) > 0

    instance = MessageProperty(Value("1234"))
    assert instance.check_is_float() is False
    assert len(instance.errors) > 0

    instance = MessageProperty(Value([]))
    assert instance.check_is_float() is False
    assert len(instance.errors) > 0

    instance = MessageProperty(Value(1234.3))
    assert instance.check_is_float() is True
    assert len(instance.errors) == 0

    instance = MessageProperty(DictValue({"test": 1234}, "wrong!!"))
    assert instance.check_is_float() is False
    assert len(instance.errors) > 0


def test_message_property_check_is_date_utc():
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


def test_message_property_properties_and_has_property():
    instance = MessageProperty(Value("1234"))
    assert not instance.has_property("test")
    with pytest.raises(KeyError):
        instance.properties("test")
    instance2 = MessageProperty(Value("1234"))
    instance.add_property("test", instance2)
    assert instance.has_property("test")
    assert instance.properties("test") == instance2


def test_message_property_can_add_property():
    instance = MessageProperty(Value("1234"))

    assert instance.property_name is None
    assert instance.property_source is None

    assert not instance.has_property("test")

    instance2 = MessageProperty(Value("1234"))

    instance.add_property("test", instance2)

    assert instance2.property_name == "test"
    assert instance2.property_source == instance
    assert instance2.property_type == "Property"
    assert instance2.property_position is None

    assert instance.has_property("test")
    assert instance.properties("test") == instance2


def test_message_property_can_add_property_when_list():
    instance = MessageProperty(Value("1234"))
    instance2 = MessageProperty(Value("1234"))
    instance3 = MessageProperty(Value("1234"))

    instance.add_property("test", [instance2, instance3])

    assert instance2.property_name == "test[0]"
    assert instance2.property_source == instance
    assert instance2.property_type == "Array"
    assert instance2.property_position == 0

    assert instance3.property_name == "test[1]"
    assert instance3.property_source == instance
    assert instance3.property_type == "Array"
    assert instance3.property_position == 1

    assert instance.has_property("test")
    assert instance.properties("test") == [instance2, instance3]


def test_message_property_trigger_error():
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
