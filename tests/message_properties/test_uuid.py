from tol_lab_share.message_properties.uuid import Uuid


def test_uuid_check_is_uuid_detects_invalid_uuid():
    instance = Uuid("1234")
    assert instance.check_is_uuid() is False


def test_uuid_check_is_uuid_detects_valid_uuid():
    instance = Uuid(b"dd490ee5-fd1d-456d-99fd-eb9d3861e0f9")
    assert instance.check_is_uuid() is True

    instance = Uuid("dd490ee5-fd1d-456d-99fd-eb9d3861e0f9")
    assert instance.check_is_uuid() is False
