from tol_lab_share.message_properties.definitions.volume import Volume
from helpers import check_validates_float_string


def test_Volume_check_Volume_is_int():
    check_validates_float_string(Volume)
