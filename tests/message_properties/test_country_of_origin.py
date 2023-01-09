from tol_lab_share.message_properties.country_of_origin import CountryOfOrigin


def test_CountryOfOrigin_check_CountryOfOrigin_is_valid():
    instance = CountryOfOrigin(None)
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = CountryOfOrigin("1234")
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = CountryOfOrigin([])
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = CountryOfOrigin(1234)
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = CountryOfOrigin("Testing")
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = CountryOfOrigin("United Kingdom")
    assert instance.validate() is True
    assert len(instance.errors) == 0
