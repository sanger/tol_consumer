import copy
import logging
from typing import Any

LEVEL_FATAL = "level_fatal"
LEVEL_ERROR = "leverl_error"
HANDLER_LOG = "handler_log"
HANDLER_RAISE = "handler_raise"

REDPANDA_SCHEMA_VALID_ORIGINS = ["parsing", "root", "plate", "sample"]

logger = logging.getLogger(__name__)


class ExceptionErrorCode(BaseException):
    """Exception class to wrap the exception generated by an error code"""

    pass


class ErrorCode:
    """Class that handles all information management and actions of an error"""

    def __init__(
        self,
        type_id: Any,
        origin: Any,
        field: Any,
        description: Any,
        level: str = LEVEL_ERROR,
        handler: str = HANDLER_LOG,
    ):
        """Constructor of an error. The arguments will define all fields to describe the error to the user,
        and also a definition of how critical the error is, and what should be the default action for it.
        Available levels of criticality are ERROR and FATAL.
        Available actions on error are log (send to default logs) or raise (trigger the error as an exception)
        """
        self.type_id = type_id
        self.field = field
        self.origin = origin
        self.description = description
        self.level = level
        self.handler = handler

    def __repr__(self) -> str:
        """Returns a textual representation of the error"""
        return self.text()

    def __str__(self) -> str:
        """Returns a textual representation of the error"""
        return self.text()

    def validate(self) -> bool:
        """Returns a boolean indicating if this error has all the information required"""
        return (
            isinstance(self.type_id, int)
            and isinstance(self.field, str)
            and isinstance(self.origin, str)
            and isinstance(self.description, str)
        )

    def text(self) -> str:
        """Returns a textual representation of the error"""
        return (
            f'(type_id="{self.type_id}", field="{self.field}", origin="{self.origin}" description="{self.description}")'
        )

    def origin_for_json(self) -> Any:
        """Classifies the origin received from the error code into one of the valid list
        of origins by the Redpanda schema.
        """
        if self.origin in REDPANDA_SCHEMA_VALID_ORIGINS:
            return self.origin
        if "sample" in self.origin:
            return "sample"
        return "root"

    def json(self) -> "dict[str, Any]":
        """Returns a JSON-like representation of the ErrorCode"""
        return {
            "typeId": self.type_id,
            "field": self.field,
            "origin": self.origin_for_json(),
            "description": self.description,
        }

    def message_for_trigger(self, text: str | None = None, instance: Any = None) -> str:
        """Generates a user-friendly message to attach to the error triggered
        Parameters:
        text (str) user friendly description of the error
        instance (Any) instance that generated the error, so the class of the instance can be
        added to the message
        Returns:
        str with the message
        """
        message = self.description
        if instance is not None:
            message += f', instance: "{type(instance).__name__}"'
        if text is not None:
            message += f', text: "{text}"'
        return str(message)

    def trigger(
        self,
        text: str | None = None,
        instance: Any = None,
        origin: str | None = None,
        field: str | None = None,
    ) -> Any:
        """Triggers the action defined for this message.
        By default, if will log all messages to the level of criticality defined in the
        default system log,. If the type of handling defined is 'raise', it will
        raise an exception.
        This method will return a new instance of ErrorCode that will be a copy of the
        original ErrorCode but with all relevant information fields updated
        Parameters:
        text (str) user-friendly error description
        instance (Any) instance that originated the error
        origin (str) origin of the error
        field (str) field where the error was originated inside the origin
        Returns:
        ErrorCode instance that will contain an updated copy of the previous error code,
        using the arguments received
        """
        message = self.message_for_trigger(text, instance)
        if self.level == LEVEL_ERROR:
            logger.error(message)
        if self.level == LEVEL_FATAL:
            logger.fatal(message)

        if self.handler == HANDLER_RAISE:
            raise ExceptionErrorCode(message)

        copied_instance = copy.deepcopy(self)
        copied_instance.description = message

        if origin:
            copied_instance.origin = origin
        if field:
            copied_instance.field = field

        return copied_instance


ERROR_1_UNKNOWN = ErrorCode(1, "plate", "unknown", "Unknown error")
ERROR_1_UUID_NOT_BINARY = ErrorCode(1, "plate", "uuid", "Uuid is not binary")
ERROR_2_UUID_NOT_RIGHT_FORMAT = ErrorCode(2, "plate", "uuid", "Uuid has wrong format")
ERROR_3_BARCODE_NOT_STRING = ErrorCode(3, "plate", "barcode", "Barcode is not a string")
ERROR_2_NOT_STRING = ErrorCode(2, "plate", "unknown", "Not string")
ERROR_3_NOT_INTEGER = ErrorCode(3, "plate", "unknown", "Not integer")
ERROR_4_NOT_VALID_COUNTRY_INSDC = ErrorCode(4, "plate", "country_of_origin", "Not a valid insdc country of origin")
ERROR_5_NOT_FLOAT = ErrorCode(5, "plate", "unknown", "Not a float")
ERROR_6_LABWARE_TYPE = ErrorCode(6, "plate", "labware type", "Not valid labware type")
ERROR_7_INVALID_LOCATION = ErrorCode(7, "plate", "locatiob", "Not valid location")
ERROR_8_INVALID_LABWARE_TYPE_FOR_LOCATION = ErrorCode(
    8, "plate", "location type", "Not valid labware type for location"
)
ERROR_9_INVALID_INPUT = ErrorCode(9, "plate", "input", "Not valid input")
ERROR_10_DICT_WRONG_KEY = ErrorCode(10, "plate", "dict", "Not valid key")
ERROR_11_PARENT_DICT_WRONG = ErrorCode(11, "plate", "dict", "Parent dict is wrong")
ERROR_12_DICT_NOT_ITERABLE = ErrorCode(12, "plate", "dict", "dict is not iterable")
ERROR_13_TRACTION_REQUEST_FAILED = ErrorCode(13, "plate", "dict", "Traction send request failed")
ERROR_14_PROBLEM_ACCESSING_TAXON_ID = ErrorCode(
    14, "plate", "taxon_id", "Problem when accessing the taxon id service", level=LEVEL_FATAL, handler=HANDLER_RAISE
)
ERROR_15_FEEDBACK_UNDEFINED_KEY = ErrorCode(
    15, "plate", "feedback", "Feedback message is missing to define some fields"
)
ERROR_16_PROBLEM_TALKING_WITH_TRACTION = ErrorCode(
    16, "root", "traction", "There was a problem while sending to traction"
)
ERROR_17_INPUT_MESSAGE_INVALID = ErrorCode(
    17, "parsing", "create-message", "There was a problem while validating the input message"
)
ERROR_18_FEEDBACK_MESSAGE_INVALID = ErrorCode(
    18,
    "parsing",
    "feedback",
    "The feedback message generated does not validate. Please contact the development team."
    "Original message will be rejected and send to the dead letters queue.",
    level=LEVEL_FATAL,
    handler=HANDLER_RAISE,
)

ERROR_19_INPUT_IS_NOT_VALID_INTEGER_STRING = ErrorCode(
    19, "parsing", "input", "The input provided is not a valid integer."
)
ERROR_20_INPUT_IS_NOT_VALID_FLOAT_STRING = ErrorCode(20, "parsing", "input", "The input provided is not a valid float.")
ERROR_21_INPUT_IS_NOT_VALID_DATE = ErrorCode(21, "parsing", "input", "The input provided is not a valid date.")
ERROR_22_CANNOT_ENCODE_FEEDBACK_MESSAGE = ErrorCode(
    22,
    "parsing",
    "feedback",
    "There was a problem while trying to encode feedback message.",
    level=LEVEL_FATAL,
    handler=HANDLER_RAISE,
)
ERROR_23_TRACTION_MESSAGE_HAS_NO_REQUESTS = ErrorCode(
    23, "parsing", "input", "The message to traction has no requests."
)
ERROR_24_TRACTION_MESSAGE_REQUESTS_HAVE_MISSING_DATA = ErrorCode(
    24, "parsing", "input", "The message to traction is missing relevant fields info."
)
ERROR_25_TRACTION_QC_MESSAGE_HAS_NO_REQUESTS = ErrorCode(
    25, "parsing", "input", "The qc message to traction has no requests."
)
ERROR_26_TRACTION_QC_MESSAGE_REQUESTS_HAVE_MISSING_DATA = ErrorCode(
    26, "parsing", "input", "The qc message to traction is missing relevant fields info."
)
ERROR_27_TRACTION_QC_REQUEST_FAILED = ErrorCode(27, "request", "dict", "Traction qc send request failed")
ERROR_28_PROBLEM_TALKING_TO_TRACTION = ErrorCode(
    28, "root", "traction", "There was a problem while sending qc message to traction"
)
ERROR_29_NOT_BOOLEAN = ErrorCode(29, "plate", "unknown", "Not a boolean")
ERROR_30_PROBLEM_TALKING_WITH_WAREHOUSE = ErrorCode(
    16, "root", "mwlh", "There was a problem while sending to warehouse"
)
ERROR_31_EMPTY_ALIQUOT = ErrorCode(29, "parsing", "aliquot", "Empty aliquot present.")
