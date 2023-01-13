import logging
from tol_lab_share.messages.output_feedback_message import OutputFeedbackMessage
from typing import List, Any, Optional
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


class MessageProperty(MessagePropertyInterface):
    def __init__(self, input):
        self._input = input
        self._errors = []
        self._properties = {}

    def validate(self):
        logger.debug("MessageProperty::validate")
        return all(list([self._validate_properties(), self._validate_instance()]))

    def properties(self, key):
        return self._properties[key]

    @cached_property
    def value(self):
        logger.debug("MessageProperty::value")
        return self._input.value

    def raise_exception(self, error_code: ErrorCode) -> None:
        self.add_error(error_code)
        raise ExceptionMessageProperty()

    def add_to_feedback_message(self, feedback_message: OutputFeedbackMessage) -> None:
        logger.debug("MessageProperty::add_to_feedback_message")
        for property in self._properties_instances:
            property.add_to_feedback_message(feedback_message)
        self.add_errors_to_feedback_message(feedback_message)

    def add_to_traction_message(self, traction_message: OutputTractionMessage) -> None:
        logger.debug("MessageProperty::add_to_traction_message")
        for property in self._properties_instances:
            property.add_to_traction_message(traction_message)

    @property
    def errors(self) -> List[ErrorCode]:
        return list(chain.from_iterable([self._errors, self._errors_properties]))

    def add_error(self, error: ErrorCode) -> None:
        self._errors.append(error.build(self.identification()))

    def identification(self):
        return type(self)

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
            self.add_error(error_codes.ERROR_9_INVALID_INPUT)
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
            self.add_error(error_codes.ERROR_2_NOT_STRING)
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
            self.add_error(error_codes.ERROR_3_NOT_INTEGER)
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
            self.add_error(error_codes.ERROR_5_NOT_FLOAT)
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
            self.add_error(error_codes.ERROR_3_NOT_INTEGER)
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
