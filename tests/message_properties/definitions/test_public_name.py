from tol_lab_share.message_properties.definitions.public_name import PublicName
from helpers import check_validates_string


def test_PublicName_check_PublicName_is_string():
    check_validates_string(PublicName)
