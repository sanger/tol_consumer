from tol_lab_share.message_properties.volume import Volume


def test_Volume_check_Volume_is_int():
    instance = Volume(None)
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = Volume("1234")
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = Volume([])
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = Volume(1234)
    assert instance.validate() is True
    assert len(instance.errors) == 0
