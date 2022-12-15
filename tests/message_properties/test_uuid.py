from tol_lab_share.message_properties.uuid import Uuid


def test_uuid_check_is_uuid_detects_invalid_uuid():
    instance = Uuid("1234")
    assert instance.check_is_uuid() is False

    instance = Uuid("dd490ee5-fd1d-456d-99fd-eb9d3861e0f9")
    assert instance.check_is_uuid() is False

    instance = Uuid("1234")
    assert instance.check_is_uuid() is False

    instance = Uuid(b"1234")
    assert instance.check_is_uuid() is False

    instance = Uuid("")
    assert instance.check_is_uuid() is False

    instance = Uuid(None)
    assert instance.check_is_uuid() is False

    instance = Uuid(1234)
    assert instance.check_is_uuid() is False

    instance = Uuid({})
    assert instance.check_is_uuid() is False


def test_uuid_check_is_uuid_detects_valid_uuid():
    instance = Uuid(b"dd490ee5-fd1d-456d-99fd-eb9d3861e0f9")
    assert instance.check_is_uuid() is True


def test_uuid_check_is_binary_when_not_binary():
    instance = Uuid("dd490ee5-fd1d-456d-99fd-eb9d3861e0f9")
    assert instance.check_is_binary() is False


def test_uuid_check_is_binary_when_is_binary():
    instance = Uuid(b"1234")
    assert instance.check_is_binary() is True

    instance = Uuid(b"dd490ee5-fd1d-456d-99fd-eb9d3861e0f9")
    assert instance.check_is_binary() is True


def test_uuid_validate_when_not_valid():
    # Not binary
    instance = Uuid("dd490ee5-fd1d-456d-99fd-eb9d3861e0f9")
    assert instance.validate() is False

    # Not valid type
    instance = Uuid(1234)
    assert instance.validate() is False


def test_uuid_validate_when_valid():
    # Not binary
    instance = Uuid(b"dd490ee5-fd1d-456d-99fd-eb9d3861e0f9")
    assert instance.validate() is True
