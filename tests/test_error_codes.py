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


def test_error_code_trigger_default_logs_error():
    instance = build_instance()
    with patch("tol_lab_share.error_codes.logger.error") as logger:
        assert isinstance(instance.trigger(), ErrorCode)
        logger.assert_called_with(instance.description)
        assert isinstance(instance.trigger("this is a test"), ErrorCode)
        logger.assert_called_with(instance.description + ": this is a test")


def test_error_code_trigger_logging_can_log():
    instance = ErrorCode(
        "my type id", "my origin", "my field", "my description", level=LEVEL_ERROR, handler=HANDLER_LOG
    )
    with patch("tol_lab_share.error_codes.logger.error") as logger:
        assert isinstance(instance.trigger(), ErrorCode)
        logger.assert_called_with(instance.description)
        assert isinstance(instance.trigger("this is a test"), ErrorCode)
        logger.assert_called_with(instance.description + ": this is a test")

    instance = ErrorCode(
        "my type id", "my origin", "my field", "my description", level=LEVEL_FATAL, handler=HANDLER_LOG
    )
    with patch("tol_lab_share.error_codes.logger.fatal") as logger:
        assert isinstance(instance.trigger(), ErrorCode)
        logger.assert_called_with(instance.description)
        assert isinstance(instance.trigger("this is a test"), ErrorCode)
        logger.assert_called_with(instance.description + ": this is a test")


def test_error_code_trigger_logging_can_raise():
    instance = ErrorCode(
        "my type id", "my origin", "my field", "my description", level=LEVEL_ERROR, handler=HANDLER_RAISE
    )
    with patch("tol_lab_share.error_codes.logger.error") as logger:
        with pytest.raises(ExceptionErrorCode):
            instance.trigger()
        logger.assert_called_with(instance.description)
        with pytest.raises(ExceptionErrorCode):
            instance.trigger("this is a test")
        logger.assert_called_with(instance.description + ": this is a test")

    instance = ErrorCode(
        "my type id", "my origin", "my field", "my description", level=LEVEL_FATAL, handler=HANDLER_RAISE
    )
    with patch("tol_lab_share.error_codes.logger.fatal") as logger:
        with pytest.raises(ExceptionErrorCode):
            instance.trigger()
        logger.assert_called_with(instance.description)
        with pytest.raises(ExceptionErrorCode):
            instance.trigger("this is a test")
        logger.assert_called_with(instance.description + ": this is a test")
