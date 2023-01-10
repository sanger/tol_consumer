from tol_lab_share.message_properties.message_property import MessageProperty
from unittest import mock
from tol_lab_share.message_properties.input import Input


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
