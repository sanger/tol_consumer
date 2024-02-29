from tol_lab_share.messages.rabbit.consumed import CreateLabwareMessage
from tol_lab_share.messages.rabbit.published import CreateLabwareFeedbackMessage


class TestCreateLabwareMessage:
    def test_validates_true_when_valid(self, valid_create_labware_message):
        subject = CreateLabwareMessage(valid_create_labware_message)
        assert subject.validate() is True
        assert len(subject.errors) == 0

    def test_validates_false_when_invalid(self, invalid_create_labware_message):
        instance = CreateLabwareMessage(invalid_create_labware_message)
        assert instance.validate() is False
        assert len(instance.errors) == 5

    def test_add_to_feedback_message_when_valid(self, valid_create_labware_message):
        subject = CreateLabwareMessage(valid_create_labware_message)
        subject.validate()
        feedback_message = CreateLabwareFeedbackMessage()

        assert feedback_message.source_message_uuid is None

        subject.add_to_message_property(feedback_message)

        assert feedback_message.source_message_uuid == "b01aa0ad-7b19-4f94-87e9-70d74fb8783c"

    def test_add_to_feedback_message_when_invalid(self, invalid_create_labware_message):
        subject = CreateLabwareMessage(invalid_create_labware_message)
        feedback_message = CreateLabwareFeedbackMessage()

        assert subject.validate() is False

        subject.add_to_message_property(feedback_message)
        assert len(feedback_message.errors) > 0
