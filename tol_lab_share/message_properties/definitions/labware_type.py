import string
from .message_property import MessageProperty
from tol_lab_share import error_codes
import logging
from typing import Callable

logger = logging.getLogger(__name__)

VALID_LABWARE_TYPES = ["Plate12x8", "Tube"]


class LabwareType(MessageProperty):
    """MessageProperty subclass to manage parsing of a valid labware type string provided by another
    MessageProperty. The labware type string has to any of these: ["Plate12x8", "Tube"]
    Eg: 'Plate12x8' for a plate
    """

    @property
    def validators(self) -> list[Callable]:
        """Defines the list of validators"""
        return [self.check_is_string, self.check_labware_type]

    def check_labware_type(self):
        """Checks that the received input contains a valid labware type. Triggers an error
        if that is not the case.
        Returns:
        bool with the result of the check
        """
        logger.debug("LabwareType::check_labware_type")
        result = self._input.value in VALID_LABWARE_TYPES
        if not result:
            self.trigger_error(error_codes.ERROR_6_LABWARE_TYPE, text=f"input: {self._input.value}")
        return result

    def valid_locations(self) -> list[str]:
        """It returns the list of valid locations for the labware type.
        If the labware type is a tube, it returns ane empty list.
        If it is a plate 12x8 it returns all locations in column order. i.e. ['A01', 'B01', 'C01', .... 'H12']

        Returns:
            list[str]: A list with all the valid locations.
        """
        if self.value == "Plate12x8":
            return [
                f"{letter}{str(number).zfill(2)}" for number in range(1, 13) for letter in string.ascii_uppercase[:8]
            ]
        else:
            return []
