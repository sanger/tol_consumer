from tol_lab_share.message_properties.concentration import Concentration


def test_Concentration_check_Concentration_is_string():
    instance = Concentration(None)
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = Concentration("1234")
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = Concentration([])
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = Concentration(1234)
    assert instance.validate() is True
    assert len(instance.errors) == 0
