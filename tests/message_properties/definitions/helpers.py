from tol_lab_share.message_properties.definitions.input import Input


def check_validates_string(klass):
    instance = klass(Input(None))
    assert instance.check_is_string() is False
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = klass(Input(1234))
    assert instance.check_is_string() is False
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = klass(Input([]))
    assert instance.check_is_string() is False
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = klass(Input("1234"))
    assert instance.check_is_string() is True
    assert instance.validate() is True
    assert len(instance.errors) == 0


def check_validates_integer(klass):
    instance = klass(Input(None))
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = klass(Input("1234"))
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = klass(Input([]))
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = klass(Input(1234))
    assert instance.validate() is True
    assert len(instance.errors) == 0


def check_validates_integer_string(klass):
    instance = klass(Input(None))
    assert instance.check_is_string() is False
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = klass(Input(1234))
    assert instance.check_is_string() is False
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = klass(Input([]))
    assert instance.check_is_string() is False
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = klass(Input("1234"))
    assert instance.check_is_string() is True
    assert instance.validate() is True
    assert len(instance.errors) == 0


def check_validates_float_string(klass):
    instance = klass(Input(None))
    assert instance.check_is_string() is False
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = klass(Input(1234))
    assert instance.check_is_string() is False
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = klass(Input([]))
    assert instance.check_is_string() is False
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = klass(Input("1234.5"))
    assert instance.check_is_string() is True
    assert instance.validate() is True
    assert len(instance.errors) == 0
