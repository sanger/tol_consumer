from tol_lab_share.messages.properties import DictValue


def test_dict_input_can_validate_when_valid():
    input = DictValue({"name": 1}, "name")
    assert input.validate()

    input = DictValue(DictValue({"name": {"first": "James"}}, "name"), "first")
    assert input.validate()


def test_dict_input_can_get_value_when_valid():
    input = DictValue({"name": 1}, "name")
    assert input.validate()


def test_dict_input_can_get_chained_value_when_valid():
    input = DictValue(DictValue({"name": {"first": "James"}}, "name"), "first")
    assert input.value == "James"


def test_dict_input_can_validate_when_invalid():
    input = DictValue({}, "name")
    assert not input.validate()

    input = DictValue({"other": 1}, "name")
    assert not input.validate()

    input = DictValue(DictValue({"name": {"first": "James"}}, "name"), "second")
    assert not input.validate()

    input = DictValue(DictValue({"name": {"first": "James"}}, "WRONG!!!"), "second")
    assert not input.validate()
