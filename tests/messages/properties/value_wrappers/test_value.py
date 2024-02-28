from tol_lab_share.messages.properties.value_wrappers import Value


def test_input_can_validate_everything_true():
    assert Value(None).validate()
    assert Value("").validate()
    assert Value([]).validate()
    assert Value("test").validate()
    assert Value(1).validate()


def test_input_can_return_value():
    assert Value(None).value is None
    assert Value("").value == ""
    assert Value([]).value == []
    assert Value("test").value == "test"
    assert Value(1).value == 1
