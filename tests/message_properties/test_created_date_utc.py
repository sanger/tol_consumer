from tol_lab_share.message_properties.created_date_utc import CreatedDateUtc

from datetime import datetime


def test_CreatedDateUtc_check_CreatedDateUtc_is_valid():
    instance = CreatedDateUtc(None)
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = CreatedDateUtc("1234")
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = CreatedDateUtc([])
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = CreatedDateUtc(1234)
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = CreatedDateUtc(1234.4)
    assert instance.validate() is True
    assert len(instance.errors) == 0

    instance = CreatedDateUtc("Testing")
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = CreatedDateUtc("United Kingdom")
    assert instance.validate() is False
    assert len(instance.errors) > 0


def test_CreatedDateUtc_check_CreatedDateUtc_value():
    instance = CreatedDateUtc(1234.4)
    assert instance.value == datetime(1970, 1, 1, 0, 20, 34, 400000)
