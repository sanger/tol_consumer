from tol_lab_share.messages.output_feedback_message import OutputFeedbackMessage
from tol_lab_share import error_codes


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


def test_output_feedback_add_error_code():
    instance = OutputFeedbackMessage()

    instance.add_error_code(error_codes.ERROR_1_UNKNOWN)
    instance.add_error_code(error_codes.ERROR_1_UNKNOWN)

    assert len(instance.errors) == 2


def test_output_feedback_validate():
    instance = OutputFeedbackMessage()
    assert not instance.validate()

    instance.count_of_total_samples = 0
    instance.count_of_valid_samples = 0
    instance.source_message_uuid = b"b01aa0ad-7b19-4f94-87e9-70d74fb8783c"
    instance.operation_was_error_free = False

    assert instance.validate()
