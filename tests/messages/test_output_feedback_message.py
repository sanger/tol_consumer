from tol_lab_share.messages.output_feedback_message import OutputFeedbackMessage
from tol_lab_share import error_codes
from lab_share_lib.rabbit.avro_encoder import AvroEncoderJson, AvroEncoderBinary

import pytest
from unittest.mock import MagicMock, patch


def test_output_feedback_message_can_instate():
    instance = OutputFeedbackMessage()
    assert instance is not None


def test_output_feedback_can_initialize():
    instance = OutputFeedbackMessage()

    assert instance.count_of_total_samples is None
    assert instance.source_message_uuid is None
    assert instance.errors == []


def test_output_feedback_can_get_and_set_props():
    instance = OutputFeedbackMessage()

    instance.count_of_total_samples = 1234
    assert instance.count_of_total_samples == 1234

    instance.source_message_uuid = b"1234"
    assert instance.source_message_uuid == b"1234"
    assert instance.errors == []


def test_output_feedback_add_error():
    instance = OutputFeedbackMessage()

    instance.add_error(error_codes.ERROR_1_UNKNOWN)
    instance.add_error(error_codes.ERROR_1_UNKNOWN)

    assert len(instance.errors) == 2


def test_output_feedback_validate():
    instance = OutputFeedbackMessage()
    assert not instance.validate()

    instance = OutputFeedbackMessage()
    instance.count_of_total_samples = 0
    instance.count_of_valid_samples = 0
    instance.source_message_uuid = b"b01aa0ad-7b19-4f94-87e9-70d74fb8783c"
    instance.operation_was_error_free = False

    assert instance.validate()


def test_output_feedback_encoder_for():
    instance = OutputFeedbackMessage()
    assert instance.encoder_config_for("json")["encoder_class"] == AvroEncoderJson
    assert instance.encoder_config_for("binary")["encoder_class"] == AvroEncoderBinary


@pytest.mark.parametrize(
    "error_code_checks",
    ["tol_lab_share.messages.output_feedback_message.error_codes.ERROR_22_CANNOT_ENCODE_FEEDBACK_MESSAGE"],
)
def test_output_feedback_publish_fails_when_not_validating_with_schema(error_code_checks, feedback_schema_json):
    publisher = MagicMock()
    exchange = "test"

    instance = OutputFeedbackMessage()
    instance.source_message_uuid = b"b01aa0ad-7b19-4f94-87e9-70d74fb8783c"
    with patch(error_code_checks) as error_code:
        schema_registry = MagicMock()
        schema_registry.get_schema.return_value = {"schema": feedback_schema_json, "version": "1"}
        instance.publish(publisher, schema_registry, exchange)

        error_code.trigger.assert_called()


def test_output_feedback_publish_fails_when_validating_with_schema(feedback_schema_json):
    publisher = MagicMock()
    exchange = "test"

    instance = OutputFeedbackMessage()
    instance.count_of_total_samples = 0
    instance.count_of_valid_samples = 0
    instance.source_message_uuid = b"b01aa0ad-7b19-4f94-87e9-70d74fb8783c"
    instance.operation_was_error_free = False

    schema_registry = MagicMock()
    schema_registry.get_schema.return_value = {"schema": feedback_schema_json, "version": "1"}
    instance.publish(publisher, schema_registry, exchange)
