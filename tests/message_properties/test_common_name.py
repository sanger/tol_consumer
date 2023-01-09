from tol_lab_share.message_properties.common_name import CommonName


def test_CommonName_check_CommonName_is_string():
    instance = CommonName(None)
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = CommonName(1234)
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = CommonName([])
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = CommonName("1234")
    assert instance.validate() is True
    assert len(instance.errors) == 0
