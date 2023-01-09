from tol_lab_share.message_properties.barcode import Barcode


def test_barcode_check_barcode_is_string():
    instance = Barcode(None)
    assert instance.check_is_string() is False
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = Barcode(1234)
    assert instance.check_is_string() is False
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = Barcode([])
    assert instance.check_is_string() is False
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = Barcode("1234")
    assert instance.check_is_string() is True
    assert instance.validate() is True
    assert len(instance.errors) == 0
