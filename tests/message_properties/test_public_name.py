from tol_lab_share.message_properties.public_name import PublicName


def test_PublicName_check_PublicName_is_string():
    instance = PublicName(None)
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = PublicName(1234)
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = PublicName([])
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = PublicName("1234")
    assert instance.validate() is True
    assert len(instance.errors) == 0
