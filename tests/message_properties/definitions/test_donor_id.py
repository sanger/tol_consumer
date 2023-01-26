from tol_lab_share.message_properties.definitions.donor_id import DonorId
from helpers import check_validates_string


def test_DonorId_check_DonorId_is_string():
    check_validates_string(DonorId)
