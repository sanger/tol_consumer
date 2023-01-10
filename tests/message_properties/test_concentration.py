from tol_lab_share.message_properties.concentration import Concentration
from helpers import check_validates_integer


def test_Concentration_check_Concentration_is_int():
    check_validates_integer(Concentration)
