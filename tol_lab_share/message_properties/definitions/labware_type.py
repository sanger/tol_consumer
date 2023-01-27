from .message_property import MessageProperty
from tol_lab_share import error_codes
import logging

logger = logging.getLogger(__name__)

VALID_LABWARE_TYPES = ["Plate12x8", "Tube"]


class LabwareType(MessageProperty):
    @property
    def validators(self):
        return [self.check_is_string, self.check_labware_type]

    def check_labware_type(self):
        logger.debug("LabwareType::check_labware_type")
        result = self._input.value in VALID_LABWARE_TYPES
        if not result:
            self.trigger_error(error_codes.ERROR_6_LABWARE_TYPE, text=f"input: {self._input.value}")
        return result

    def pad_number(self, number):
        padded_number = str(number)
        if len(padded_number) == 1:
            padded_number = f"0{padded_number}"
        return padded_number

    def _locations_for_plate12x8_column_order(self):
        locations = []
        for number in range(12):
            for letter_ord in range(ord("A"), ord("H") + 1):
                locations.append(f"{chr(letter_ord)}{self.pad_number(number+1)}")
        return locations

    def valid_locations(self):
        if self.value == "Plate12x8":
            return self._locations_for_plate12x8_column_order()
        else:
            return []
