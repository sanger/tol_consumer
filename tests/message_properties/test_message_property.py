from tol_lab_share.message_properties.message_property import MessageProperty
from unittest import mock
from tol_lab_share.message_properties.input import Input
from tol_lab_share import error_codes
import pytest


def test_message_property_can_initialize():
    instance = MessageProperty(Input("1234"))
    assert instance is not None


def test_message_property_state_machine_can_validate():
    instance = MessageProperty(Input("1234"))
    assert instance.validate() is True

    with mock.patch(
        "tol_lab_share.message_properties.message_property.MessageProperty.validators", new_callable=mock.PropertyMock
    ) as mock_my_property:
        mock_my_property.return_value = [lambda: False]

        assert instance.validate() is False


def test_message_property_state_machine_can_get_value():
    instance = MessageProperty(Input("1234"))
    assert instance.value == "1234"


def test_message_property_check_is_string():
    instance = MessageProperty(Input("1234"))
    assert instance.check_is_string() is True

    instance = MessageProperty(Input(b"dd490ee5-fd1d-456d-99fd-eb9d3861e0f9"))
    assert instance.check_is_string() is False

    instance = MessageProperty(Input(""))
    assert instance.check_is_string() is True

    instance = MessageProperty(Input(None))
    assert instance.check_is_string() is False

    instance = MessageProperty(Input(1234))
    assert instance.check_is_string() is False

    instance = MessageProperty(Input({}))
    assert instance.check_is_string() is False


def test_message_property_check_is_integer():
    instance = MessageProperty(Input(None))
    assert instance.check_is_integer() is False
    assert len(instance.errors) > 0

    instance = MessageProperty(Input("1234"))
    assert instance.check_is_integer() is False
    assert len(instance.errors) > 0

    instance = MessageProperty(Input([]))
    assert instance.check_is_integer() is False
    assert len(instance.errors) > 0

    instance = MessageProperty(Input(1234))
    assert instance.check_is_integer() is True
    assert len(instance.errors) == 0


def test_message_property_check_is_float():
    instance = MessageProperty(Input(None))
    assert instance.check_is_float() is False
    assert len(instance.errors) > 0

    instance = MessageProperty(Input("1234"))
    assert instance.check_is_float() is False
    assert len(instance.errors) > 0

    instance = MessageProperty(Input([]))
    assert instance.check_is_float() is False
    assert len(instance.errors) > 0

    instance = MessageProperty(Input(1234.3))
    assert instance.check_is_float() is True
    assert len(instance.errors) == 0


def test_message_property_check_is_date_utc():
    instance = MessageProperty(Input("1234"))
    assert instance.check_is_date_utc() is False

    instance = MessageProperty(Input(b"dd490ee5-fd1d-456d-99fd-eb9d3861e0f9"))
    assert instance.check_is_date_utc() is False

    instance = MessageProperty(Input(""))
    assert instance.check_is_date_utc() is False

    instance = MessageProperty(Input(None))
    assert instance.check_is_date_utc() is False

    instance = MessageProperty(Input(1234))
    assert instance.check_is_date_utc() is True

    instance = MessageProperty(Input({}))
    assert instance.check_is_date_utc() is False


def test_message_property_properties_and_has_property():
    instance = MessageProperty(Input("1234"))
    assert not instance.has_property("test")
    with pytest.raises(KeyError):
        instance.properties("test")
    instance2 = MessageProperty(Input("1234"))
    instance.add_property("test", instance2)
    assert instance.has_property("test")
    assert instance.properties("test") == instance2


def test_message_property_can_add_property():
    instance = MessageProperty(Input("1234"))

    assert instance.property_name is None
    assert instance.property_source is None

    assert not instance.has_property("test")

    instance2 = MessageProperty(Input("1234"))

    instance.add_property("test", instance2)

    assert instance2.property_name == "test"
    assert instance2.property_source == instance

    assert instance.has_property("test")
    assert instance.properties("test") == instance2


def test_message_property_trigger_error():
    error = error_codes.ERROR_1_UNKNOWN
    instance = MessageProperty(Input("1234"))
    assert len(instance.errors) == 0
    instance.trigger_error(error)
    assert len(instance.errors) == 1
    instance.trigger_error(error.trigger(text="1234"))
    assert len(instance.errors) == 2
    assert instance.errors[1].field == error.field

    instance1 = MessageProperty(Input("1234"))
    instance2 = MessageProperty(Input("1234"))
    instance3 = MessageProperty(Input("1234"))
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
