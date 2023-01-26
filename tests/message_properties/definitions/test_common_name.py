from tol_lab_share.message_properties.definitions.common_name import CommonName
from helpers import check_validates_string


def test_CommonName_check_CommonName_is_string():
    check_validates_string(CommonName)
