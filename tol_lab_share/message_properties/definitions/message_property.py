from __future__ import annotations
import datetime
import logging
from functools import cached_property, singledispatchmethod
from itertools import chain
from typing import Any, Callable, Dict, List, Optional, Union, cast

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
        self._errors: List[ErrorCode] = []
        self._properties: Dict[str, Any] = {}
        self.property_name: str | None = None
        self.property_source: MessageProperty | None = None
        self.property_position: int | None = None
        self.property_type: str = PROPERTY_TYPE_PROPERTY

    def validate(self) -> bool:
        return self._validation_status

    @cached_property
    def _validation_status(self) -> bool:
        """Runs all validations in both the internal properties and in the instance itself, and
        returns a boolean with the result.
        Returns:
        bool with the result of all validations aggregated
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

    def _add_property_list(self, property_name: str, input: List[MessageProperty]) -> None:
        """Given a property name and a list of message properties, it stores this list of MessageProperty
        as the value of the property and includes the position in each of them.
        Parameters:
        property_name (str) name of the property
        input (List[MessagePropertyInterface]) list of message properties
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

    def add_property(self, property_name: str, input: Union[MessageProperty, List[MessageProperty]]) -> None:
        """Given an property name and an input it adds the input as the value of the property
        Parameters:
        property_name (str) name of the property
        input (MessagePropertyInterface |  List[MessagePropertyInterface]) property or list of
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

    def trigger_error(self, error_code: ErrorCode, text: Optional[str] = None) -> None:
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
    def errors(self) -> List[ErrorCode]:
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
    def validators(self) -> List[Callable]:
        """Defines the list of validators"""
        return []

    def check_is_valid_input(self) -> bool:
        """Checks that the input provided value can pass all its internal validations.
        Triggers an error if not
        Returns:
        bool with the result
        """
        logger.debug("MessageProperty::check_is_valid_input")
        result = self._input.validate()
        if not result:
            self.trigger_error(error_codes.ERROR_9_INVALID_INPUT)
        return cast(bool, result)

    def check_is_string(self) -> bool:
        """Checks that the input provided value is an instance of a string.
        Triggers an error if not
        Returns:
        bool with the result
        """
        logger.debug("MessageProperty::check_is_string")
        if not self.check_is_valid_input():
            return False
        result = isinstance(self._input.value, str)
        if not result:
            self.trigger_error(error_codes.ERROR_2_NOT_STRING)
        return result

    def check_is_integer(self) -> bool:
        """Checks that the input provided value is an instance of an integer.
        Triggers an error if not
        Returns:
        bool with the result
        """
        logger.debug("MessageProperty::check_is_integer")
        if not self.check_is_valid_input():
            return False

        result = isinstance(self._input.value, int)
        if not result:
            self.trigger_error(error_codes.ERROR_3_NOT_INTEGER)
        return result

    def check_is_integer_string(self) -> bool:
        """Checks that the input provided value is an integer string.
        Triggers an error if not
        Returns:
        bool with the result
        """
        logger.debug("MessageProperty::check_is_integer_string")
        if not self.check_is_string():
            return False

        result = None
        try:
            result = int(self._input.value)
        except ValueError:
            pass
        if result is None:
            self.trigger_error(error_codes.ERROR_19_INPUT_IS_NOT_VALID_INTEGER_STRING)
        return result is not None

    def check_is_float_string(self) -> bool:
        """Checks that the input provided value is a float string.
        Triggers an error if not
        Returns:
        bool with the result
        """
        logger.debug("MessageProperty::check_is_float_string")
        if not self.check_is_string():
            return False

        result = None
        try:
            result = float(self._input.value)
        except ValueError:
            pass
        if result is None:
            self.trigger_error(error_codes.ERROR_20_INPUT_IS_NOT_VALID_FLOAT_STRING)
        return result is not None

    def check_is_float(self) -> bool:
        """Checks that the input provided value is an instance of a float.
        Triggers an error if not
        Returns:
        bool with the result
        """
        logger.debug("MessageProperty::check_is_float")
        if not self.check_is_valid_input():
            return False

        result = isinstance(self._input.value, float)
        if not result:
            self.trigger_error(error_codes.ERROR_5_NOT_FLOAT)
        return result

    def check_is_date_utc(self) -> bool:
        """Checks that the input provided value is an instance of a datetime.
        Triggers an error if not
        Returns:
        bool with the result
        """
        logger.debug("MessageProperty::check_is_date_utc")
        if not self.check_is_valid_input():
            return False

        result = isinstance(self._input.value, datetime.datetime)
        if not result:
            self.trigger_error(error_codes.ERROR_21_INPUT_IS_NOT_VALID_DATE_UTC)
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
    def _errors_properties(self) -> List[ErrorCode]:
        """Returns a list that contains all the errors for the properties inside this
        instance.
        Returns:
        List[ErrorCode] with all the errors from the properties
        """
        error_list = []
        for property in self._properties_instances:
            if len(property.errors) > 0:
                for error in property.errors:
                    error_list.append(error)
        return error_list

    @cached_property
    def _properties_instances(self) -> List[MessageProperty]:
        """Returns a list that contains all the properties inside this
        instance.
        Returns:
        List[MessagePropertyInterface] with all the properties
        """
        prop_list = []
        for property in list(self._properties.values()):
            if isinstance(property, list):
                for elem in list(property):
                    prop_list.append(elem)
            else:
                prop_list.append(property)
        return prop_list
