import copy


class ErrorCode:
    def __init__(self, type_id, origin, field, description):
        self.type_id = type_id
        self.field = field
        self.origin = origin
        self.description = description

    def __repr__(self):
        return self.text()

    def __str__(self):
        return self.text()

    def validate(self):
        return (
            isinstance(self.type_id, str)
            and isinstance(self.field, str)
            and isinstance(self.origin, str)
            and isinstance(self.description, str)
        )

    def with_description(self, description):
        instance = copy.deepcopy(self)
        instance.description = description

        return instance

    def text(self):
        return f"type_id={self.type_id}, field={self.field}, origin={self.origin} description={self.description}"

    def json(self):
        return {
            "type_id": self.type_id,
            "field": self.field,
            "origin": self.origin,
            "description": self.description,
        }


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
ERROR_14_PROBLEM_ACCESSING_TAXON_ID = ErrorCode(14, "plate", "taxon_id", "Problem when accessing the taxon id service")
ERROR_15_FEEDBACK_UNDEFINED_KEY = ErrorCode(
    15, "plate", "feedback", "Feedback message is missing to define some fields"
)
