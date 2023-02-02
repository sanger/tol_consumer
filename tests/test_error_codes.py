from tol_lab_share.error_codes import (
    ErrorCode,
    LEVEL_ERROR,
    LEVEL_FATAL,
    HANDLER_LOG,
    HANDLER_RAISE,
    ExceptionErrorCode,
)
from unittest.mock import patch
import pytest


def build_instance():
    return ErrorCode(1, "root", "my field", "my description")


def test_error_code_init():
    assert build_instance() is not None


def test_error_code_validate():
    instance = ErrorCode(1, 2, 3, 4)
    assert not instance.validate()

    instance = build_instance()
    assert instance.validate()


def test_error_code_can_convert_to_str():
    instance = build_instance()
    assert str(instance) == '(type_id="1", field="my field", origin="root" description="my description")'


def test_error_code_json():
    instance = build_instance()
    assert instance.json() == {
        "description": "my description",
        "field": "my field",
        "origin": "root",
        "typeId": 1,
    }


def test_message_for_trigger():
    instance = build_instance()
    assert instance.message_for_trigger() == "my description"
    assert instance.message_for_trigger(text="one more thing") == 'my description, text: "one more thing"'
    assert instance.message_for_trigger(instance=instance) == 'my description, instance: "ErrorCode"'
    assert (
        instance.message_for_trigger(text="one more thing", instance=instance)
        == 'my description, instance: "ErrorCode", text: "one more thing"'
    )


def test_error_code_trigger_default_behaviour():
    instance = build_instance()
    with patch.object(instance, "message_for_trigger") as mocked_message_method:
        with patch("tol_lab_share.error_codes.logger.error") as logger:
            # It returns an ErrorCode
            assert isinstance(instance.trigger(), ErrorCode)
            # It logs error by default
            logger.assert_called_with(instance.message_for_trigger())
            # It uses default messge
            mocked_message_method.assert_called_with()
            # It can trigger with an optional text
            assert isinstance(instance.trigger("this is a test"), ErrorCode)
            # It generates the message from the text
            mocked_message_method.assert_called_with("this is a test", None)
            # It can trigger with an optional instance
            assert isinstance(instance.trigger(instance=instance), ErrorCode)
            # It generates a message from the instance by default
            mocked_message_method.assert_called_with(None, instance)
            # It can trigger with both instance and text
            assert isinstance(instance.trigger(instance=instance, text="my text"), ErrorCode)
            # It generates the message using this two args
            mocked_message_method.assert_called_with("my text", instance)


def test_error_code_trigger_replicates_original_copy():
    instance = build_instance()
    instance2 = instance.trigger()
    assert instance2 != instance
    assert instance.description == instance2.description
    instance3 = instance.trigger("my new text")
    assert instance3.description != instance.description


def test_error_code_trigger_can_setup_origin_and_field():
    instance = build_instance()
    instance2 = instance.trigger("my new text", origin="a new origin", field="field modified")
    assert instance.origin != instance2.origin
    assert instance.field != instance2.field
    assert instance2.origin == "a new origin"
    assert instance2.field == "field modified"

    # It does not overwrite when not defined
    instance3 = instance.trigger("my other new text")
    assert instance3.field == instance.field
    assert instance3.origin == instance.origin


def test_error_code_trigger_logging_can_log():
    instance = ErrorCode("my type id", "root", "my field", "my description", level=LEVEL_ERROR, handler=HANDLER_LOG)
    with patch("tol_lab_share.error_codes.logger.error") as logger:
        assert isinstance(instance.trigger(), ErrorCode)
        logger.assert_called_with(instance.message_for_trigger())
        assert isinstance(instance.trigger("this is a test"), ErrorCode)
        logger.assert_called_with(instance.message_for_trigger("this is a test"))

    instance = ErrorCode("my type id", "root", "my field", "my description", level=LEVEL_FATAL, handler=HANDLER_LOG)
    with patch("tol_lab_share.error_codes.logger.fatal") as logger:
        assert isinstance(instance.trigger(), ErrorCode)
        logger.assert_called_with(instance.message_for_trigger())
        assert isinstance(instance.trigger("this is a test"), ErrorCode)
        logger.assert_called_with(instance.message_for_trigger("this is a test"))


def test_error_code_trigger_logging_can_raise():
    instance = ErrorCode("my type id", "root", "my field", "my description", level=LEVEL_ERROR, handler=HANDLER_RAISE)
    with patch("tol_lab_share.error_codes.logger.error") as logger:
        with pytest.raises(ExceptionErrorCode):
            instance.trigger()
        logger.assert_called_with(instance.message_for_trigger())
        with pytest.raises(ExceptionErrorCode):
            instance.trigger("this is a test")
        logger.assert_called_with(instance.message_for_trigger("this is a test"))

    instance = ErrorCode("my type id", "root", "my field", "my description", level=LEVEL_FATAL, handler=HANDLER_RAISE)
    with patch("tol_lab_share.error_codes.logger.fatal") as logger:
        with pytest.raises(ExceptionErrorCode):
            instance.trigger()
        logger.assert_called_with(instance.message_for_trigger())
        with pytest.raises(ExceptionErrorCode):
            instance.trigger("this is a test")
        logger.assert_called_with(instance.message_for_trigger("this is a test"))
