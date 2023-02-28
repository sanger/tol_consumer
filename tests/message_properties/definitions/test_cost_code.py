from tol_lab_share.message_properties.definitions.cost_code import CostCode
from helpers import check_validates_string


def test_CostCode_check_CostCode_is_string():
    check_validates_string(CostCode)
