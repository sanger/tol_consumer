from tol_lab_share.message_properties.definitions.taxon_id import TaxonId
from helpers import check_validates_integer_string


def test_TaxonId_check_TaxonId_is_int():
    check_validates_integer_string(TaxonId)
