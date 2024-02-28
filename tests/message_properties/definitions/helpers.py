from tol_lab_share.messages.properties.value_wrappers import Value


def check_validates_string(klass):
    instance = klass(Value(None))
    assert instance.check_is_string() is False
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = klass(Value(1234))
    assert instance.check_is_string() is False
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = klass(Value([]))
    assert instance.check_is_string() is False
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = klass(Value("1234"))
    assert instance.check_is_string() is True
    assert instance.validate() is True
    assert len(instance.errors) == 0


def check_validates_integer_string(klass):
    instance = klass(Value(None))
    assert instance.check_is_string() is False
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = klass(Value(1234))
    assert instance.check_is_string() is False
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = klass(Value([]))
    assert instance.check_is_string() is False
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = klass(Value("1234"))
    assert instance.check_is_string() is True
    assert instance.validate() is True
    assert len(instance.errors) == 0


def check_validates_float_string(klass):
    instance = klass(Value(None))
    assert instance.check_is_string() is False
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = klass(Value(1234))
    assert instance.check_is_string() is False
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = klass(Value([]))
    assert instance.check_is_string() is False
    assert instance.validate() is False
    assert len(instance.errors) > 0

    instance = klass(Value("1234.5"))
    assert instance.check_is_string() is True
    assert instance.validate() is True
    assert len(instance.errors) == 0
