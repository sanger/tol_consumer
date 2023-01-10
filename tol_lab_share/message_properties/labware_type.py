from .message_property import MessageProperty
from tol_lab_share import error_codes
import logging

logger = logging.getLogger(__name__)

VALID_LABWARE_TYPE = ["Plate12x8", "Tube"]


class LabwareType(MessageProperty):
    @property
    def validators(self):
        return [self.check_is_string, self.check_labware_type]

    def check_labware_type(self):
        logger.debug("MessageProperty::check_labware_type")
        result = False
        try:
            result = VALID_LABWARE_TYPE.index(self._input) >= 0
        except AttributeError:
            pass
        except ValueError:
            pass
        if not result:
            self.add_error(error_codes.ERROR_6_LABWARE_TYPE)
        return result

    def pad_number(self, number):
        padded_number = str(number)
        if len(padded_number) == 1:
            padded_number = f"0{padded_number}"
        return padded_number

    def _locations_for_plate12x8_row_order(self):
        locations = []
        for letter_ord in range(ord("A"), ord("H") + 1):
            for number in range(12):
                locations.append(f"{chr(letter_ord)}{self.pad_number(number+1)}")
        return locations

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
