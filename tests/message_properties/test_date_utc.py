from tol_lab_share.message_properties.date_utc import DateUtc

from datetime import datetime
from tol_lab_share.message_properties.input import Input


def test_DateUtc_check_DateUtc_is_valid():
    instance = DateUtc(Input(None))
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = DateUtc(Input("1234"))
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = DateUtc(Input([]))
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = DateUtc(Input(1234))
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = DateUtc(Input(datetime(1970, 1, 1, 0, 20, 34, 400000)))
    assert instance.validate() is True
    assert len(instance.errors) == 0

    instance = DateUtc(Input("Testing"))
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = DateUtc(Input("United Kingdom"))
    assert instance.validate() is False
    assert len(instance.errors) > 0


def test_DateUtc_check_DateUtc_value():
    instance = DateUtc(Input(datetime(1970, 1, 1, 0, 20, 34, 400000)))
    assert instance.value == datetime(1970, 1, 1, 0, 20, 34, 400000)
