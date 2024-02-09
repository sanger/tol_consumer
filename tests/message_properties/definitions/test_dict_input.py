from tol_lab_share.message_properties.definitions.dict_input import dictInput


def test_dict_input_can_validate_when_valid():
    input = dictInput({"name": 1}, "name")
    assert input.validate()

    input = dictInput(dictInput({"name": {"first": "James"}}, "name"), "first")
    assert input.validate()


def test_dict_input_can_get_value_when_valid():
    input = dictInput({"name": 1}, "name")
    assert input.validate()


def test_dict_input_can_get_chained_value_when_valid():
    input = dictInput(dictInput({"name": {"first": "James"}}, "name"), "first")
    assert input.value == "James"


def test_dict_input_can_validate_when_invalid():
    input = dictInput({}, "name")
    assert not input.validate()

    input = dictInput({"other": 1}, "name")
    assert not input.validate()

    input = dictInput(dictInput({"name": {"first": "James"}}, "name"), "second")
    assert not input.validate()

    input = dictInput(dictInput({"name": {"first": "James"}}, "WRONG!!!"), "second")
    assert not input.validate()
