from tol_lab_share.message_properties.taxon_id import TaxonId


def test_TaxonId_check_TaxonId_is_int():
    instance = TaxonId(None)
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = TaxonId("1234")
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = TaxonId([])
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = TaxonId(1234)
    assert instance.validate() is True
    assert len(instance.errors) == 0
