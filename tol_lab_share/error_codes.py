import copy


class ErrorCode:
    def __init__(self, type_id, origin, field, description):
        self.type_id = type_id
        self.field = field
        self.origin = origin
        self.description = description
        self.identification = None

    def __str__(self):
        return f"{self.type_id}, {self.field} {self.origin} {self.description} { self.identification }"

    def build(self, identification):
        instance = copy.deepcopy(self)
        instance.identification = identification
        return instance


ERROR_1_UNKNOWN = ErrorCode(1, "plate", "unknown", "Unknown error")
ERROR_1_UUID_NOT_BINARY = ErrorCode(1, "plate", "uuid", "Uuid is not binary")
ERROR_2_UUID_NOT_RIGHT_FORMAT = ErrorCode(2, "plate", "uuid", "Uuid has wrong format")
ERROR_3_BARCODE_NOT_STRING = ErrorCode(3, "plate", "barcode", "Barcode is not a string")
ERROR_2_NOT_STRING = ErrorCode(2, "plate", "unknown", "Not string")
ERROR_3_NOT_INTEGER = ErrorCode(3, "plate", "unknown", "Not integer")
ERROR_4_NOT_VALID_COUNTRY_INSDC = ErrorCode(4, "plate", "country_of_origin", "Not a valid insdc country of origin")
ERROR_5_NOT_FLOAT = ErrorCode(5, "plate", "unknown", "Not a float")
ERROR_6_LABWARE_TYPE = ErrorCode(6, "plate", "labware type", "Not valid labware type")
