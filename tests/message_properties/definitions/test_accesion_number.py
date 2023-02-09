from tol_lab_share.message_properties.definitions.accession_number import AccessionNumber
from helpers import check_validates_string


def test_accession_number_is_string():
    check_validates_string(AccessionNumber)
