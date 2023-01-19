import logging
from tol_lab_share.messages.output_feedback_message import OutputFeedbackMessage
from typing import List, Any, Optional, Union
from tol_lab_share.error_codes import ErrorCode
from functools import cached_property
from tol_lab_share.messages.output_traction_message import OutputTractionMessage
from itertools import chain
from tol_lab_share import error_codes
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class ExceptionMessageProperty(BaseException):
    pass


class MessagePropertyInterface(ABC):
    @abstractmethod
    def validate(self):
        ...

    @property
    @abstractmethod
    def errors(self) -> Any:
        ...

    @cached_property
    @abstractmethod
    def value(self) -> Optional[Any]:
        ...

    @abstractmethod
    def add_to_feedback_message(self, feedback_message: OutputFeedbackMessage) -> None:
        ...

    @abstractmethod
    def add_to_traction_message(self, traction_message: OutputTractionMessage) -> None:
        ...

    @property
    @abstractmethod
    def property_name(self) -> Optional[str]:
        ...

    @property_name.setter
    @abstractmethod
    def property_name(self, value: str) -> None:
        ...

    @property
    @abstractmethod
    def property_source(self) -> Optional[Any]:
        ...

    @property_source.setter
    @abstractmethod
    def property_source(self, value: Any) -> None:
        ...

    @property
    @abstractmethod
    def property_position(self) -> Optional[int]:
        ...

    @property_position.setter
    @abstractmethod
    def property_position(self, value: Any) -> None:
        ...

    @property
    @abstractmethod
    def property_type(self) -> Optional[str]:
        ...

    @property_type.setter
    @abstractmethod
    def property_type(self, value: Any) -> None:
        ...


class MessageProperty(MessagePropertyInterface):
    def __init__(self, input):
        self._input = input
        self._errors = []
        self._properties = {}
        self.property_name = None
        self.property_source = None
        self.property_position = None
        self.property_type = "Property"

    def validate(self):
        return all(list([self._validate_properties(), self._validate_instance()]))

    def properties(self, key):
        return self._properties[key]

    def has_property(self, key):
        return key in self._properties

    def _add_property_instance(self, property_name: str, instance: MessagePropertyInterface) -> None:
        if not hasattr(self, "_properties"):
            self._properties = {}
        instance.property_name = property_name
        instance.property_source = self
        instance.property_position = None
        instance.property_type = "Property"
        self._properties[property_name] = instance

    def _add_property_list(self, property_name: str, input: List[MessagePropertyInterface]) -> None:
        self._properties[property_name] = []
        for pos in range(len(input)):
            instance = input[pos]
            instance.property_name = property_name
            instance.property_source = self
            instance.property_position = pos
            instance.property_type = "Array"
            self._properties[property_name].append(instance)

    def add_property(
        self, property_name: str, input: Union[MessagePropertyInterface, List[MessagePropertyInterface]]
    ) -> None:
        if isinstance(input, list):
            self._add_property_list(property_name, input)
        else:
            self._add_property_instance(property_name, input)

    @property
    def property_name(self) -> Optional[str]:
        return self._property_name

    @property_name.setter
    def property_name(self, value: str) -> None:
        self._property_name = value

    @property
    def property_source(self) -> Optional[MessagePropertyInterface]:
        return self._property_source

    @property_source.setter
    def property_source(self, value: MessagePropertyInterface) -> None:
        self._property_source = value

    @property
    def property_position(self) -> Optional[int]:
        return self._property_position

    @property_position.setter
    def property_position(self, value: int) -> None:
        self._property_position = value

    @property
    def property_type(self) -> Optional[str]:
        return self._property_type

    @property_type.setter
    def property_type(self, value: str) -> None:
        self._property_type = value

    @cached_property
    def value(self):
        return self._input.value

    def raise_exception(self, error_code: ErrorCode) -> None:
        self.add_error(error_code)
        raise ExceptionMessageProperty()

    @property
    def origin(self):
        if self.property_source:
            return self.property_source.property_name
        return None

    @property
    def field(self):
        return self.property_name

    def trigger_error(self, error_code: ErrorCode, text: Optional[str] = None) -> None:
        self.add_error(error_code.trigger(instance=self, origin=self.origin, field=self.field, text=text))

    def add_to_feedback_message(self, feedback_message: OutputFeedbackMessage) -> None:
        for property in self._properties_instances:
            property.add_to_feedback_message(feedback_message)
        self.add_errors_to_feedback_message(feedback_message)

    def add_to_traction_message(self, traction_message: OutputTractionMessage) -> None:
        for property in self._properties_instances:
            property.add_to_traction_message(traction_message)

    @property
    def errors(self) -> List[ErrorCode]:
        return list(chain.from_iterable([self._errors, self._errors_properties]))

    def add_error(self, error: ErrorCode) -> None:
        self._errors.append(error)

    def add_errors_to_feedback_message(self, feedback_message: OutputFeedbackMessage) -> None:
        for error in self.errors:
            feedback_message.add_error_code(error)

    @property
    def validators(self):
        return []

    def check_is_valid_input(self):
        logger.debug("MessageProperty::check_is_valid_input")
        result = False
        try:
            result = self._input.validate()
        except AttributeError:
            pass
        except KeyError:
            pass
        if not result:
            self.trigger_error(error_codes.ERROR_9_INVALID_INPUT)
        return result

    def check_is_string(self):
        logger.debug("MessageProperty::check_is_string")
        if not self.check_is_valid_input():
            return False
        result = False
        try:
            result = isinstance(self._input.value, str)
        except AttributeError:
            pass
        if not result:
            self.trigger_error(error_codes.ERROR_2_NOT_STRING)
        return result

    def check_is_integer(self):
        logger.debug("MessageProperty::check_is_integer")
        if not self.check_is_valid_input():
            return False

        result = False
        try:
            result = isinstance(self._input.value, int)
        except AttributeError:
            pass
        if not result:
            self.trigger_error(error_codes.ERROR_3_NOT_INTEGER)
        return result

    def check_is_float(self):
        logger.debug("MessageProperty::check_is_float")
        if not self.check_is_valid_input():
            return False

        result = False
        try:
            result = isinstance(self._input.value, float)
        except AttributeError:
            pass
        if not result:
            self.trigger_error(error_codes.ERROR_5_NOT_FLOAT)
        return result

    def check_is_date_utc(self):
        logger.debug("MessageProperty::check_is_date_utc")
        if not self.check_is_valid_input():
            return False

        result = False
        try:
            result = isinstance(self._input.value, int)
        except AttributeError:
            pass
        if not result:
            self.trigger_error(error_codes.ERROR_3_NOT_INTEGER)
        return result

    def _validate_properties(self):
        return all(list([property.validate() for property in self._properties_instances]))

    def _validate_instance(self):
        return all(list([validator() for validator in self.validators]))

    @property
    def default_error_code(self):
        return error_codes.ERROR_1_UNKNOWN

    @property
    def _errors_properties(self) -> List[ErrorCode]:
        error_list = []
        for property in self._properties_instances:
            if len(property.errors) > 0:
                for error in property.errors:
                    error_list.append(error)
        return error_list

    @cached_property
    def _properties_instances(self) -> List[MessagePropertyInterface]:
        prop_list = []
        for property in list(self._properties.values()):
            if isinstance(property, list):
                for elem in list(property):
                    prop_list.append(elem)
            else:
                prop_list.append(property)
        return prop_list
