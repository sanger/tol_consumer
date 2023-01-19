from tol_lab_share.message_properties.concentration import Concentration
from helpers import check_validates_float_string


def test_Concentration_check_Concentration_is_int():
    check_validates_float_string(Concentration)
