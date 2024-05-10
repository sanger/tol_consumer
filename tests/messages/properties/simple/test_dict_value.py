from tol_lab_share.messages.properties.simple.dict_value import DictValue


class TestDictValue:
    def test_validates_true_when_valid_input(self):
        subject = DictValue({"name": 1}, "name")
        assert subject.validate() is True

        subject = DictValue(DictValue({"name": {"first": "James"}}, "name"), "first")
        assert subject.validate() is True

    def test_can_get_value_when_valid(self):
        subject = DictValue({"name": 1}, "name")
        assert subject.validate() is True

    def test_can_get_chained_value_when_valid(self):
        subject = DictValue(DictValue({"name": {"first": "James"}}, "name"), "first")
        assert subject.value == "James"

    def test_can_validate_when_invalid(self):
        subject = DictValue({}, "name")
        assert subject.validate() is False

        subject = DictValue({"other": 1}, "name")
        assert subject.validate() is False

        subject = DictValue(DictValue({"name": {"first": "James"}}, "name"), "second")
        assert subject.validate() is False

        subject = DictValue(DictValue({"name": {"first": "James"}}, "WRONG!!!"), "second")
        assert subject.validate() is False

    def test_validates_true_when_optional(self):
        subject = DictValue({"first_name": "James"}, "first_name", optional=True)
        assert subject.validate() is True

        subject = DictValue({"first_name": "James"}, "last_name", optional=True)
        assert subject.validate() is True

    def test_can_get_value_when_optional(self):
        subject = DictValue({"first_name": "James"}, "first_name", optional=True)
        assert subject.value == "James"

        subject = DictValue({"first_name": "James"}, "last_name", optional=True)
        assert subject.value is None
