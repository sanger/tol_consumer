from tol_lab_share.message_properties.message_property import MessageProperty


def test_message_property_can_initialize():
    instance = MessageProperty("1234")
    assert instance is not None


def test_message_property_state_machine_can_validate():
    instance = MessageProperty("1234")
    assert instance.validate() is True

    instance._validators = [lambda: False]
    assert instance.validate() is False


def test_message_property_state_machine_can_get_value():
    instance = MessageProperty("1234")
    assert instance.value == "1234"


def test_message_property_check_is_string():
    instance = MessageProperty("1234")
    assert instance.check_is_string() is True

    instance = MessageProperty(b"dd490ee5-fd1d-456d-99fd-eb9d3861e0f9")
    assert instance.check_is_string() is False

    instance = MessageProperty("")
    assert instance.check_is_string() is True

    instance = MessageProperty(None)
    assert instance.check_is_string() is False

    instance = MessageProperty(1234)
    assert instance.check_is_string() is False

    instance = MessageProperty({})
    assert instance.check_is_string() is False
