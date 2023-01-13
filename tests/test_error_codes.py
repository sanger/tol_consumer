from tol_lab_share.error_codes import ErrorCode


def build_instance():
    return ErrorCode("my type id", "my origin", "my field", "my description")


def test_error_code_init():
    assert build_instance() is not None


def test_error_code_validate():
    instance = ErrorCode(1, 2, 3, 4)
    assert not instance.validate()

    instance = build_instance()
    assert instance.validate()


def test_error_code_json():
    instance = build_instance()
    assert instance.json() == {
        "description": "my description",
        "field": "my field",
        "origin": "my origin",
        "type_id": "my type id",
    }


def test_error_code_with_description():
    instance = build_instance().with_description("this is a test")
    assert instance.json() == {
        "description": "this is a test",
        "field": "my field",
        "origin": "my origin",
        "type_id": "my type id",
    }


def test_error_code_with_description_does_not_overwrite_definition():
    instance = build_instance()
    assert instance.json() == {
        "description": "my description",
        "field": "my field",
        "origin": "my origin",
        "type_id": "my type id",
    }

    instance = build_instance().with_description("this is a test")
    assert instance.json() == {
        "description": "this is a test",
        "field": "my field",
        "origin": "my origin",
        "type_id": "my type id",
    }

    instance = build_instance()
    assert instance.json() == {
        "description": "my description",
        "field": "my field",
        "origin": "my origin",
        "type_id": "my type id",
    }
