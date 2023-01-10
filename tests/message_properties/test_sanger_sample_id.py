from tol_lab_share.message_properties.sanger_sample_id import SangerSampleId
from helpers import check_validates_string


def test_SangerSampleId_check_SangerSampleId_is_string():
    check_validates_string(SangerSampleId)
