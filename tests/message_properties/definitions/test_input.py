from tol_lab_share.message_properties.definitions.input import Input


def test_input_can_validate_everything_true():
    assert Input(None).validate()
    assert Input("").validate()
    assert Input([]).validate()
    assert Input("test").validate()
    assert Input(1).validate()


def test_input_can_return_value():
    assert Input(None).value is None
    assert Input("").value == ""
    assert Input([]).value == []
    assert Input("test").value == "test"
    assert Input(1).value == 1
