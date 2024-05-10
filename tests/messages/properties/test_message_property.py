from tol_lab_share.messages.properties import MessageProperty
from unittest import mock
from tol_lab_share.messages.properties.simple.dict_value import DictValue
from tol_lab_share.messages.properties.simple.value import Value
from tol_lab_share import error_codes
import pytest
from datetime import datetime, UTC


class TestMessageProperty:
    def test_can_validate(self):
        instance = MessageProperty(Value("1234"))
        assert instance.validate() is True

        instance = MessageProperty(Value("1234"))
        with mock.patch(
            "tol_lab_share.messages.properties.MessageProperty.validators",
            new_callable=mock.PropertyMock,
        ) as mock_my_property:
            mock_my_property.return_value = [lambda: False]

            assert instance.validate() is False

    def test_can_retrieve_value(self):
        value = "1234"
        instance = MessageProperty(Value(value))
        assert instance.value == value

    def test_check_is_float_accepts_float(self):
        instance = MessageProperty(Value(1234.0))
        assert instance.check_is_float() is True
        assert len(instance.errors) == 0

    @pytest.mark.parametrize(
        "input_value",
        ["1234.0", [], {}, b"1234.0", 1234, datetime.now(UTC), DictValue({"test": 1234}, "wrong!!")],
        ids=[
            "a string",
            "a list",
            "a dictionary",
            "binary data",
            "an integer",
            "datetime",
            "an invalid message property",
        ],
    )
    def test_check_is_float_rejects(self, input_value):
        instance = MessageProperty(Value(input_value))
        assert instance.check_is_float() is False
        assert len(instance.errors) > 0

    @pytest.mark.parametrize("optional", [True, False])
    def test_integer_checker_accepts_an_integer(self, optional):
        instance = MessageProperty(Value(1234))
        assert instance.integer_checker(optional=optional)() is True
        assert len(instance.errors) == 0

    def test_integer_checker_accepts_none_when_optional(self):
        instance = MessageProperty(Value(None))
        assert instance.integer_checker(optional=True)() is True
        assert len(instance.errors) == 0

    @pytest.mark.parametrize(
        "input_value",
        ["1234", [], {}, b"1234", 1234.0, datetime.now(UTC), DictValue({"test": 1234}, "wrong!!")],
        ids=[
            "string integer",
            "a list",
            "a dictionary",
            "binary data",
            "a float",
            "datetime",
            "an invalid message property",
        ],
    )
    @pytest.mark.parametrize("optional", [True, False], ids=["optional", "not optional"])
    def test_integer_checker_rejects(self, input_value, optional):
        instance = MessageProperty(Value(input_value))
        assert instance.integer_checker(optional=optional)() is False
        assert len(instance.errors) > 0

    def test_integer_checker_rejects_none_when_not_optional(self):
        instance = MessageProperty(Value(None))
        assert instance.integer_checker(optional=False)() is False
        assert len(instance.errors) > 0

    def test_integer_checker_rejects_none_with_default_optional_flag(self):
        instance = MessageProperty(Value(None))
        assert instance.integer_checker()() is False
        assert len(instance.errors) > 0

    @pytest.mark.parametrize(
        "input_value",
        ["1234", ""],
        ids=["a populated string", "an empty string"],
    )
    @pytest.mark.parametrize("optional", [True, False])
    def test_string_checker_accepts(self, input_value, optional):
        instance = MessageProperty(Value(input_value))
        assert instance.string_checker(optional=optional)() is True
        assert len(instance.errors) == 0

    def test_string_checker_accepts_none_when_optional(self):
        instance = MessageProperty(Value(None))
        assert instance.string_checker(optional=True)() is True
        assert len(instance.errors) == 0

    @pytest.mark.parametrize(
        "input_value",
        [[], {}, b"1234", 1234, 1234.0, datetime.now(UTC), DictValue({"test": 1234}, "wrong!!")],
        ids=[
            "a list",
            "a dictionary",
            "binary data",
            "an integer",
            "a float",
            "datetime",
            "an invalid message property",
        ],
    )
    @pytest.mark.parametrize("optional", [True, False])
    def test_string_checker_rejects(self, input_value, optional):
        instance = MessageProperty(Value(input_value))
        assert instance.string_checker(optional=optional)() is False
        assert len(instance.errors) > 0

    def test_string_checker_rejects_none_when_not_optional(self):
        instance = MessageProperty(Value(None))
        assert instance.string_checker(optional=False)() is False
        assert len(instance.errors) > 0

    def test_string_checker_rejects_none_with_default_optional_flag(self):
        instance = MessageProperty(Value(None))
        assert instance.string_checker()() is False
        assert len(instance.errors) > 0

    def test_check_is_datetime_accepts_datetime(self):
        instance = MessageProperty(Value(datetime.now(UTC)))
        assert instance.check_is_datetime() is True
        assert len(instance.errors) == 0

    @pytest.mark.parametrize(
        "input_value",
        ["14/02/2024", [], {}, b"14/02/2024", 1234, 1234.0, DictValue({"test": 1234}, "wrong!!")],
        ids=[
            "a string",
            "a list",
            "a dictionary",
            "binary data",
            "an integer",
            "a float",
            "an invalid message property",
        ],
    )
    def test_check_is_datetime_rejects(self, input_value):
        instance = MessageProperty(Value(input_value))
        assert instance.check_is_datetime() is False
        assert len(instance.errors) > 0

    def test_has_property(self):
        instance = MessageProperty(Value("1234"))
        assert not instance.has_property("test")

        instance.add_property("test", Value("5678"))
        assert instance.has_property("test")

    def test_properties(self):
        instance = MessageProperty(Value("1234"))
        with pytest.raises(KeyError):
            instance.properties("test")

        child_value = Value("5678")
        instance.add_property("test", child_value)
        assert instance.properties("test") == child_value

    def test_can_add_property(self):
        instance = MessageProperty(Value("1234"))

        assert instance.property_name is None
        assert instance.property_source is None

        assert not instance.has_property("test")

        child_value = Value("5678")

        instance.add_property("test", child_value)

        assert child_value.property_name == "test"
        assert child_value.property_source == instance
        assert child_value.property_type == "Property"
        assert child_value.property_position is None

        assert instance.has_property("test")
        assert instance.properties("test") == child_value

    def test_can_add_properties_in_a_list(self):
        instance = MessageProperty(Value("1234"))
        child1 = Value("5678")
        child2 = Value("9012")

        instance.add_property("test", [child1, child2])

        assert child1.property_name == "test[0]"
        assert child1.property_source == instance
        assert child1.property_type == "Array"
        assert child1.property_position == 0

        assert child2.property_name == "test[1]"
        assert child2.property_source == instance
        assert child2.property_type == "Array"
        assert child2.property_position == 1

        assert instance.has_property("test")
        assert instance.properties("test") == [child1, child2]

    def test_trigger_error(self):
        error = error_codes.ERROR_1_UNKNOWN
        instance = MessageProperty(Value("1234"))
        assert len(instance.errors) == 0
        instance.trigger_error(error)
        assert len(instance.errors) == 1
        instance.trigger_error(error.trigger(text="1234"))
        assert len(instance.errors) == 2
        assert instance.errors[1].field == error.field

        instance1 = MessageProperty(Value("1234"))
        instance2 = MessageProperty(Value("1234"))
        instance3 = MessageProperty(Value("1234"))
        instance1.add_property("labware", instance2)
        instance2.add_property("sample", instance3)

        instance1.trigger_error(error)
        instance2.trigger_error(error)
        instance3.trigger_error(error)

        assert instance1.errors[0].field == error.field
        assert instance1.errors[0].origin == error.origin

        assert instance2.errors[0].field == "labware"
        assert instance2.errors[0].origin == error.origin

        assert instance3.errors[0].field == "sample"
        assert instance3.errors[0].origin == "labware"
