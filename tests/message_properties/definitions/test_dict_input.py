from tol_lab_share.message_properties.definitions.dict_input import DictInput


def test_dict_input_can_validate_when_valid():
    input = DictInput({"name": 1}, "name")
    assert input.validate()

    input = DictInput(DictInput({"name": {"first": "James"}}, "name"), "first")
    assert input.validate()


def test_dict_input_can_get_value_when_valid():
    input = DictInput({"name": 1}, "name")
    assert input.validate()


def test_dict_input_can_get_chained_value_when_valid():
    input = DictInput(DictInput({"name": {"first": "James"}}, "name"), "first")
    assert input.value == "James"


def test_dict_input_can_validate_when_invalid():
    input = DictInput({}, "name")
    assert not input.validate()

    input = DictInput(None, "name")
    assert not input.validate()

    input = DictInput([], "name")
    assert not input.validate()

    input = DictInput({"other": 1}, "name")
    assert not input.validate()

    input = DictInput(DictInput({"name": {"first": "James"}}, "name"), "second")
    assert not input.validate()
