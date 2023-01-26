from tol_lab_share.message_properties.definitions.uuid import Uuid
from tol_lab_share.message_properties.definitions.input import Input


def test_uuid_check_is_uuid_detects_invalid_uuid():
    instance = Uuid(Input("1234"))
    assert instance.check_is_uuid() is False
    assert instance.validate() is False

    instance = Uuid(Input("dd490ee5-fd1d-456d-99fd-eb9d3861e0f9"))
    assert instance.check_is_uuid() is False
    assert instance.validate() is False

    instance = Uuid(Input("1234"))
    assert instance.check_is_uuid() is False
    assert instance.validate() is False

    instance = Uuid(Input(b"1234"))
    assert instance.check_is_uuid() is False
    assert instance.validate() is False

    instance = Uuid(Input(""))
    assert instance.check_is_uuid() is False
    assert instance.validate() is False

    instance = Uuid(Input(None))
    assert instance.check_is_uuid() is False
    assert instance.validate() is False

    instance = Uuid(Input(1234))
    assert instance.check_is_uuid() is False
    assert instance.validate() is False

    instance = Uuid(Input({}))
    assert instance.check_is_uuid() is False
    assert instance.validate() is False


def test_uuid_check_is_uuid_detects_valid_uuid():
    instance = Uuid(Input(b"dd490ee5-fd1d-456d-99fd-eb9d3861e0f9"))
    assert instance.check_is_uuid() is True
    assert instance.validate() is True


def test_uuid_check_is_binary_when_not_binary():
    instance = Uuid(Input("dd490ee5-fd1d-456d-99fd-eb9d3861e0f9"))
    assert instance.check_is_binary() is False
    assert instance.validate() is False


def test_uuid_check_is_binary_when_is_binary():
    instance = Uuid(Input(b"1234"))
    assert instance.check_is_binary() is True
    assert instance.validate() is False

    instance = Uuid(Input(b"dd490ee5-fd1d-456d-99fd-eb9d3861e0f9"))
    assert instance.check_is_binary() is True
    assert instance.validate() is True


def test_validate_when_not_valid():
    # Not binary
    instance = Uuid(Input("dd490ee5-fd1d-456d-99fd-eb9d3861e0f9"))
    assert instance.validate() is False

    # Not valid type
    instance = Uuid(Input(1234))
    assert instance.validate() is False

    assert len(instance.errors) > 0


def test_uuid_validate_when_valid():
    # Not binary
    instance = Uuid(Input(b"dd490ee5-fd1d-456d-99fd-eb9d3861e0f9"))
    assert instance.validate() is True
