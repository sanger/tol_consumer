from tol_lab_share.message_properties.volume import Volume
from helpers import check_validates_integer


def test_Volume_check_Volume_is_int():
    check_validates_integer(Volume)
