from __future__ import annotations
import datetime
import logging
from functools import cached_property, singledispatchmethod
from itertools import chain
from typing import Any, Callable, cast

from tol_lab_share import error_codes
from tol_lab_share.error_codes import ErrorCode

logger = logging.getLogger(__name__)

PROPERTY_TYPE_PROPERTY = "Property"
PROPERTY_TYPE_ARRAY = "Array"


class MessageProperty:
    """Base class for MessageProperty that provides the core functionality of
    running validations, managing properties, triggering errors and some common
    validation checks.
    """

    def __init__(self, input: Any):
        """Constructor that receives a MessageProperty instance and initializes this
        instance resetting errors, empty properties and initial values for it.
        Parameters:
        input (MessagePropertyInterface) An instance of message property that we will use as base
        """
        self._input = input
        self._errors: list[ErrorCode] = []
        self._properties: dict[str, Any] = {}
        self.property_name: str | None = None
        self.property_source: MessageProperty | None = None
        self.property_position: int | None = None
        self.property_type: str = PROPERTY_TYPE_PROPERTY

    def validate(self) -> bool:
        return self._cached_validation

    @cached_property
    def _cached_validation(self) -> bool:
        """Runs validations on all the instance properties and on the instance itself.

        Returns:
            True is all validations pass, False otherwise.
        """
        return all(list([self._validate_properties(), self._validate_instance()]))

    def properties(self, key: str) -> Any:
        """Returns the property stored for the key provided"""
        return self._properties[key]

    def has_property(self, key):
        """Returns a boolean indicating if the property exists for the key provided"""
        return key in self._properties

    def _add_property_instance(self, property_name: str, instance: MessageProperty) -> None:
        """Given a property name and an instance of MessageProperty, it configures this instance as
        the value for the property.
        Parameters:
        property_name (str) name of the property to set
        instance (MessagePropertyInterface) instance of message property we want to set
        """
        instance.property_name = property_name
        instance.property_source = self
        instance.property_position = None
        instance.property_type = PROPERTY_TYPE_PROPERTY
        self._properties[property_name] = instance

    def _property_name_for_list_instance(self, property_name: str, pos: int) -> str:
        """Returns the name of the property including the position for an instance inside a property
        that contain a list.
        Parameters:
        property_name (str) name of the property
        pos (int) position inside the list
        Returns:
        str with name that represents the property name and the position
        """
        return f"{property_name}[{pos}]"

    def _add_property_list(self, property_name: str, input: list[MessageProperty]) -> None:
        """Given a property name and a list of message properties, it stores this list of MessageProperty
        as the value of the property and includes the position in each of them.
        Parameters:
        property_name (str) name of the property
        input (list[MessagePropertyInterface]) list of message properties
        Returns:
        None
        """
        self._properties[property_name] = []
        for pos in range(len(input)):
            instance = input[pos]
            instance.property_name = self._property_name_for_list_instance(property_name, pos)
            instance.property_source = self
            instance.property_position = pos
            instance.property_type = PROPERTY_TYPE_ARRAY
            self._properties[property_name].append(instance)

    def add_property(self, property_name: str, input: MessageProperty | list[MessageProperty]) -> None:
        """Given an property name and an input it adds the input as the value of the property
        Parameters:
        property_name (str) name of the property
        input (MessagePropertyInterface |  list[MessagePropertyInterface]) property or list of
        properties that we want to add for the name provided
        Returns:
        None
        """
        if isinstance(input, list):
            self._add_property_list(property_name, input)
        else:
            self._add_property_instance(property_name, input)

    @cached_property
    def value(self) -> Any:
        """Returns the value representing this property."""
        return self._input.value

    @property
    def origin(self) -> Any:
        """Returns the property name of the property source (the name of the property that contains the
        container of this property)."""
        if self.property_source:
            return self.property_source.property_name
        return None

    @property
    def field(self):
        """Alias to property name"""
        return self.property_name

    def trigger_error(self, error_code: ErrorCode, text: str | None = None) -> None:
        """Given an error instance, it performs the action associated with it and after that it adds
        the error to the list of errors defined for the current property.
        Parameters:
        error_code (ErrorCode) instance of error that we want to trigger
        text (str) an optional string with a more detailed description of the error experienced
        Returns:
        None
        """
        self.add_error(error_code.trigger(instance=self, origin=self.origin, field=self.field, text=text))

    @singledispatchmethod
    def add_to_message_property(self, message_property: MessageProperty) -> None:
        """Adds the information from child properties of this property to the message provided.

        Args:
            message_property (MessageProperty): The message property to add the information to.
        """
        for property in self._properties_instances:
            property.add_to_message_property(message_property)

    @property
    def errors(self) -> list[ErrorCode]:
        """Returns an aggregation of all errors from the current instance and all errors from
        the properties it contains.
        """
        return list(chain.from_iterable([self._errors, self._errors_properties]))

    def add_error(self, error: ErrorCode) -> None:
        """Adds an error to the list of errors of the current instance.
        Parameters:
        error (ErrorCode) Error we want to add
        """
        self._errors.append(error)

    @property
    def validators(self) -> list[Callable]:
        """Defines the list of validators"""
        return []

    def check_is_valid_input(self) -> bool:
        """Validates that the provided input passes its own validity checks.  When the validity of the input is False,
        an "invalid input" error is triggered:

        Returns:
            bool: True if the input is valid, False otherwise.
        """
        logger.debug("MessageProperty::check_is_valid_input")
        result = self._input.validate()
        if not result:
            self.trigger_error(error_codes.ERROR_9_INVALID_INPUT)
        return cast(bool, result)

    def check_is_boolean(self) -> bool:
        """Validates that the input value is a boolean. Note that other values that can represent a boolean, such as 0
        for False and -1 or 1 for True, are not acceptable. When the value cannot be identified as a boolean, a "not
        boolean" error is triggered:

        Returns:
            bool: True if the input value is a boolean, False otherwise.
        """
        logger.debug("MessageProperty::check_is_boolean")
        if not self.check_is_valid_input():
            return False

        result = isinstance(self._input.value, bool)
        if not result:
            self.trigger_error(error_codes.ERROR_29_NOT_BOOLEAN)
        return result

    def check_is_float(self) -> bool:
        """Validates that the input value is a float. Note that other numeric types that can be expressed as a float are
        not acceptable. When the value cannot be identified as a float, a "not float" error is triggered:

        Returns:
            bool: True if the input value is a float, False otherwise.
        """
        logger.debug("MessageProperty::check_is_float")
        if not self.check_is_valid_input():
            return False

        result = isinstance(self._input.value, float)
        if not result:
            self.trigger_error(error_codes.ERROR_5_NOT_FLOAT)
        return result

    def integer_checker(self, optional: bool = False) -> Callable:
        """Provides a check method that validates that the input value is an integer. When the check method is called
        and either of the following conditions are identified, a "not integer" error is triggered:

        - The input value is not an integer.
        - The input value is None and the optional flag is False.

        Parameters:
            optional (bool) flag that indicates if the input value can be None.

        Returns:
            Callable: A function that checks if the input value is an integer.
        """

        def check_is_integer() -> bool:
            logger.debug("MessageProperty::check_is_integer")
            if not self.check_is_valid_input():
                return False

            # Booleans are instances of int, so we need to explicitly exclude them
            result = (isinstance(self._input.value, int) and not type(self._input.value) is bool) or (
                optional and self._input.value is None
            )
            if not result:
                self.trigger_error(error_codes.ERROR_3_NOT_INTEGER)
            return result

        return check_is_integer

    def string_checker(self, optional: bool = False) -> Callable:
        """Provides a check method that validates that the input value is a string. When the check method is called and
        either of the following conditions are identified, a "not string" error is triggered:

        - The input value is not a string.
        - The input value is None and the optional flag is False.

        Parameters:
            optional (bool) flag that indicates if the input value can be None.

        Returns:
            Callable: A function that checks if the input value is a string.
        """

        def check_is_string() -> bool:
            logger.debug("MessageProperty::check_is_string")
            if not self.check_is_valid_input():
                return False
            result = isinstance(self._input.value, str) or (optional and self._input.value is None)
            if not result:
                self.trigger_error(error_codes.ERROR_2_NOT_STRING)
            return result

        return check_is_string

    def check_is_datetime(self) -> bool:
        """Validates that the input value is a datetime object. Note that other types such as strings containing a date
        and/or time are not acceptable. When the value cannot be identified as a datetime, a "not valid date" error is
        triggered:

        Returns:
            bool: True if the input value is a datetime, False otherwise.
        """
        logger.debug("MessageProperty::check_is_datetime")
        if not self.check_is_valid_input():
            return False

        result = isinstance(self._input.value, datetime.datetime)
        if not result:
            self.trigger_error(error_codes.ERROR_21_INPUT_IS_NOT_VALID_DATE)
        return result

    def _validate_properties(self) -> bool:
        """Validates all internal properties and returns the result
        Returns:
        bool with the result
        """
        return all(list([property.validate() for property in self._properties_instances]))

    def _validate_instance(self) -> bool:
        """Validates all validators from current instance and returns the result
        Returns:
        bool with the result
        """
        return all(list([validator() for validator in self.validators]))

    @property
    def _errors_properties(self) -> list[ErrorCode]:
        """Returns a list that contains all the errors for the properties inside this
        instance.
        Returns:
        list[ErrorCode] with all the errors from the properties
        """
        error_list = []
        for property in self._properties_instances:
            if len(property.errors) > 0:
                for error in property.errors:
                    error_list.append(error)
        return error_list

    @cached_property
    def _properties_instances(self) -> list[MessageProperty]:
        """Returns a list that contains all the properties inside this
        instance.
        Returns:
        list[MessagePropertyInterface] with all the properties
        """
        prop_list = []
        for property in list(self._properties.values()):
            if isinstance(property, list):
                for elem in list(property):
                    prop_list.append(elem)
            else:
                prop_list.append(property)
        return prop_list
