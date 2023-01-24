import logging
import copy

LEVEL_FATAL = "level_fatal"
LEVEL_ERROR = "leverl_error"
HANDLER_LOG = "handler_log"
HANDLER_RAISE = "handler_raise"

logger = logging.getLogger(__name__)


class ExceptionErrorCode(BaseException):
    pass


class ErrorCode:
    def __init__(self, type_id, origin, field, description, level=LEVEL_ERROR, handler=HANDLER_LOG):
        self.type_id = type_id
        self.field = field
        self.origin = origin
        self.description = description
        self.level = level
        self.handler = handler

    def __repr__(self):
        return self.text()

    def __str__(self):
        return self.text()

    def validate(self):
        return (
            isinstance(self.type_id, int)
            and isinstance(self.field, str)
            and isinstance(self.origin, str)
            and isinstance(self.description, str)
        )

    def text(self):
        return (
            f'(type_id="{self.type_id}", field="{self.field}", origin="{self.origin}" description="{self.description}")'
        )

    def json(self):
        return {
            "type_id": self.type_id,
            "field": self.field,
            "origin": self.origin,
            "description": self.description,
        }

    def message_for_trigger(self, text=None, instance=None):
        message = self.description
        if instance is not None:
            message += ', instance: "' + str(type(instance).__name__) + '"'
        if text is not None:
            message += ', text: "' + text + '"'
        return message

    def trigger(self, text=None, instance=None, origin=None, field=None):
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
ERROR_12_DICT_NOT_ITERABLE = ErrorCode(12, "plate", "dict", "Dict is not iterable")
ERROR_13_TRACTION_REQUEST_FAILED = ErrorCode(13, "plate", "dict", "Traction send request failed")
ERROR_14_PROBLEM_ACCESSING_TAXON_ID = ErrorCode(
    14, "plate", "taxon_id", "Problem when accessing the taxon id service", level=LEVEL_FATAL, handler=HANDLER_RAISE
)
ERROR_15_FEEDBACK_UNDEFINED_KEY = ErrorCode(
    15, "plate", "feedback", "Feedback message is missing to define some fields"
)
ERROR_16_PROBLEM_TALKING_WITH_TRACTION = ErrorCode(
    16, "message", "traction", "There was a problem while sending to traction"
)
ERROR_17_INPUT_MESSAGE_INVALID = ErrorCode(
    17, "message", "create-message", "There was a problem while validating the input message"
)
ERROR_18_FEEDBACK_MESSAGE_INVALID = ErrorCode(
    18,
    "message",
    "feedback",
    "The feedback message generated does not validate. Please contact the development team."
    "Original message will be rejected and send to the dead letters queue.",
    level=LEVEL_FATAL,
    handler=HANDLER_RAISE,
)

ERROR_19_INPUT_IS_NOT_VALID_INTEGER_STRING = ErrorCode(
    19, "input", "input", "The input provided is not a valid integer."
)
ERROR_20_INPUT_IS_NOT_VALID_FLOAT_STRING = ErrorCode(20, "input", "input", "The input provided is not a valid float.")
ERROR_21_INPUT_IS_NOT_VALID_DATE_UTC = ErrorCode(21, "input", "input", "The input provided is not a valid date.")
