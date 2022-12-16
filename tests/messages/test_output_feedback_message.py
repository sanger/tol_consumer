from tol_lab_share.messages.output_feedback_message import OutputFeedbackMessage


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


def test_output_feedback_add_error_add_errors():
    instance = OutputFeedbackMessage()

    instance.add_error(
        type_id=1, origin="sample", sample_uuid=b"1234", field="sample_name", description="An error when writing..."
    )
    instance.add_error(
        type_id=2, origin="plate", sample_uuid=None, field="barcode", description="An error when writing (again)..."
    )

    assert instance.errors == [
        [1, "sample", b"1234", "sample_name", "An error when writing..."],
        [2, "plate", None, "barcode", "An error when writing (again)..."],
    ]
