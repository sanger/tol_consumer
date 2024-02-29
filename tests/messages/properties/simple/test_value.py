from tol_lab_share.messages.properties.simple import Value


class TestValue:
    def test_can_validate_anything_as_true(self):
        assert Value(None).validate()
        assert Value("").validate()
        assert Value([]).validate()
        assert Value("test").validate()
        assert Value(1).validate()

    def test_can_retrieve_value(self):
        assert Value(None).value is None
        assert Value("").value == ""
        assert Value([]).value == []
        assert Value("test").value == "test"
        assert Value(1).value == 1
