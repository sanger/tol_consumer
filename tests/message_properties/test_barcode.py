from tol_lab_share.message_properties.barcode import Barcode
from helpers import check_validates_string


def test_barcode_check_barcode_is_string():
    check_validates_string(Barcode)
