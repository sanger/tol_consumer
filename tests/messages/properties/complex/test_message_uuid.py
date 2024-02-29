from tol_lab_share.messages.properties.complex import MessageUuid
from tol_lab_share.messages.properties.simple import Value
from tol_lab_share.messages.rabbit.published import CreateLabwareFeedbackMessage


class TestMessageUuid:
    def test_add_to_create_labware_feedback_message(self):
        instance = MessageUuid(Value(b"dd490ee5-fd1d-456d-99fd-eb9d3861e0f9"))
        feedback = CreateLabwareFeedbackMessage()

        instance.validate()
        instance.add_to_message_property(feedback)

        assert feedback.operation_was_error_free is True
        assert feedback.source_message_uuid == "dd490ee5-fd1d-456d-99fd-eb9d3861e0f9"
