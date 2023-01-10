from tol_lab_share.message_properties.taxon_id import TaxonId
from helpers import check_validates_integer


def test_TaxonId_check_TaxonId_is_int():
    check_validates_integer(TaxonId)
