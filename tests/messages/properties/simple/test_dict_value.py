from tol_lab_share.messages.properties.simple.dict_value import DictValue


class TestDictValue:
    def test_can_validate_when_valid(self):
        input = DictValue({"name": 1}, "name")
        assert input.validate()

        input = DictValue(DictValue({"name": {"first": "James"}}, "name"), "first")
        assert input.validate()

    def test_can_get_value_when_valid(self):
        input = DictValue({"name": 1}, "name")
        assert input.validate()

    def test_can_get_chained_value_when_valid(self):
        input = DictValue(DictValue({"name": {"first": "James"}}, "name"), "first")
        assert input.value == "James"

    def test_can_validate_when_invalid(self):
        input = DictValue({}, "name")
        assert not input.validate()

        input = DictValue({"other": 1}, "name")
        assert not input.validate()

        input = DictValue(DictValue({"name": {"first": "James"}}, "name"), "second")
        assert not input.validate()

        input = DictValue(DictValue({"name": {"first": "James"}}, "WRONG!!!"), "second")
        assert not input.validate()
