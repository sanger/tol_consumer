from tol_lab_share.messages.message import Message
from tol_lab_share import error_codes


def test_can_add_errors():
    message = Message()
    message.add_error_code(error_codes.ERROR_1_UNKNOWN)
    message.add_error_code(error_codes.ERROR_2_NOT_STRING)

    assert len(message.errors) == 2


def test_can_validate():
    message = Message()

    assert message.validate()
