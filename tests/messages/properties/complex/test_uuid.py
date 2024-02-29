from tol_lab_share.messages.properties.complex import Uuid
from tol_lab_share.messages.properties.simple import Value


class TestUuid:
    def test_validators_accept_valid_uuid(self):
        # Not binary
        instance = Uuid(Value(b"dd490ee5-fd1d-456d-99fd-eb9d3861e0f9"))
        assert instance.validate() is True

    def test_validators_reject_invalid_uuid(self):
        # Not binary
        instance = Uuid(Value("dd490ee5-fd1d-456d-99fd-eb9d3861e0f9"))
        assert instance.validate() is False

        # Not valid type
        instance = Uuid(Value(1234))
        assert instance.validate() is False

        assert len(instance.errors) > 0

    def test_check_is_uuid_detects_valid_uuids(self):
        instance = Uuid(Value(b"dd490ee5-fd1d-456d-99fd-eb9d3861e0f9"))
        assert instance.check_is_uuid() is True

        instance = Uuid(Value(b"28c96f02-a15c-11ed-b8de-fa163e1e3ca9"))
        assert instance.check_is_uuid() is True

    def test_check_is_uuid_detects_invalid_uuids(self):
        instance = Uuid(Value("1234"))
        assert instance.check_is_uuid() is False

        instance = Uuid(Value("dd490ee5-fd1d-456d-99fd-eb9d3861e0f9"))
        assert instance.check_is_uuid() is False

        instance = Uuid(Value("1234"))
        assert instance.check_is_uuid() is False

        instance = Uuid(Value(b"1234"))
        assert instance.check_is_uuid() is False

        instance = Uuid(Value(""))
        assert instance.check_is_uuid() is False

        instance = Uuid(Value(None))
        assert instance.check_is_uuid() is False

        instance = Uuid(Value(1234))
        assert instance.check_is_uuid() is False

        instance = Uuid(Value({}))
        assert instance.check_is_uuid() is False

    def test_check_is_binary_detects_binary_values(self):
        instance = Uuid(Value(b"1234"))
        assert instance.check_is_binary() is True
        assert instance.validate() is False

        instance = Uuid(Value(b"dd490ee5-fd1d-456d-99fd-eb9d3861e0f9"))
        assert instance.check_is_binary() is True
        assert instance.validate() is True

    def test_check_is_binary_detects_non_binary_value(self):
        instance = Uuid(Value("dd490ee5-fd1d-456d-99fd-eb9d3861e0f9"))
        assert instance.check_is_binary() is False
