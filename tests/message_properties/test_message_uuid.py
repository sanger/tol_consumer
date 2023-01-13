from tol_lab_share.message_properties.message_uuid import MessageUuid
from tol_lab_share.messages.output_feedback_message import OutputFeedbackMessage
from tol_lab_share.message_properties.input import Input


def test_uuid_add_to_feedback_message():
    instance = MessageUuid(Input(b"dd490ee5-fd1d-456d-99fd-eb9d3861e0f9"))
    feedback = OutputFeedbackMessage()

    instance.validate()
    instance.add_to_feedback_message(feedback)

    assert feedback.operation_was_error_free is True
    assert feedback.source_message_uuid == "dd490ee5-fd1d-456d-99fd-eb9d3861e0f9"
