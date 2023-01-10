from tol_lab_share.message_properties.dict_input import DictInput


def test_dict_input_can_validate_when_valid():
    input = DictInput({"name": 1}, "name")
    assert input.validate()


def test_dict_input_can_validate_when_invalid():
    input = DictInput({}, "name")
    assert not input.validate()

    input = DictInput(None, "name")
    assert not input.validate()

    input = DictInput([], "name")
    assert not input.validate()

    input = DictInput({"other": 1}, "name")
    assert not input.validate()
