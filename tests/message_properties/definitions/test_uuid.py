from tol_lab_share.message_properties.definitions.uuid import Uuid
from tol_lab_share.messages.properties import Value


def test_uuid_check_is_uuid_detects_invalid_uuid():
    instance = Uuid(Value("1234"))
    assert instance.check_is_uuid() is False
    assert instance.validate() is False

    instance = Uuid(Value("dd490ee5-fd1d-456d-99fd-eb9d3861e0f9"))
    assert instance.check_is_uuid() is False
    assert instance.validate() is False

    instance = Uuid(Value("1234"))
    assert instance.check_is_uuid() is False
    assert instance.validate() is False

    instance = Uuid(Value(b"1234"))
    assert instance.check_is_uuid() is False
    assert instance.validate() is False

    instance = Uuid(Value(""))
    assert instance.check_is_uuid() is False
    assert instance.validate() is False

    instance = Uuid(Value(None))
    assert instance.check_is_uuid() is False
    assert instance.validate() is False

    instance = Uuid(Value(1234))
    assert instance.check_is_uuid() is False
    assert instance.validate() is False

    instance = Uuid(Value({}))
    assert instance.check_is_uuid() is False
    assert instance.validate() is False


def test_uuid_check_is_uuid_detects_valid_uuid():
    instance = Uuid(Value(b"dd490ee5-fd1d-456d-99fd-eb9d3861e0f9"))
    assert instance.check_is_uuid() is True
    assert instance.validate() is True

    instance = Uuid(Value(b"28c96f02-a15c-11ed-b8de-fa163e1e3ca9"))
    assert instance.check_is_uuid() is True
    assert instance.validate() is True


def test_uuid_check_is_binary_when_not_binary():
    instance = Uuid(Value("dd490ee5-fd1d-456d-99fd-eb9d3861e0f9"))
    assert instance.check_is_binary() is False
    assert instance.validate() is False


def test_uuid_check_is_binary_when_is_binary():
    instance = Uuid(Value(b"1234"))
    assert instance.check_is_binary() is True
    assert instance.validate() is False

    instance = Uuid(Value(b"dd490ee5-fd1d-456d-99fd-eb9d3861e0f9"))
    assert instance.check_is_binary() is True
    assert instance.validate() is True


def test_validate_when_not_valid():
    # Not binary
    instance = Uuid(Value("dd490ee5-fd1d-456d-99fd-eb9d3861e0f9"))
    assert instance.validate() is False

    # Not valid type
    instance = Uuid(Value(1234))
    assert instance.validate() is False

    assert len(instance.errors) > 0


def test_uuid_validate_when_valid():
    # Not binary
    instance = Uuid(Value(b"dd490ee5-fd1d-456d-99fd-eb9d3861e0f9"))
    assert instance.validate() is True
