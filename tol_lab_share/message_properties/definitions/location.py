from .message_property import MessageProperty
from tol_lab_share import error_codes
from functools import cached_property
from typing import Any
from typing import List, Callable

import logging

logger = logging.getLogger(__name__)


class Location(MessageProperty):
    """MessageProperty subclass to manage parsing of a valid location string provided by another
    MessageProperty.
    The location has to be valid corresponding with the labware type that this instance is related
    to.
    """

    @cached_property
    def value(self):
        """Returns the value of this location unpadded.
        Eg: 'A1'
        """
        if self._input.value is None:
            return None

        return self.unpadded()

    @property
    def validators(self) -> List[Callable]:
        """Defines the list of validators"""
        return [self.check_is_location]

    def sample(self) -> Any:
        """Returns the sample where this location is defined.
        Return:
        MessagePropertyInterface: sample
        """
        return self.property_source

    def labware(self):
        """Returns the labware where this location is defined.
        Return:
        MessagePropertyInterface: labware
        """
        return self.sample().property_source

    def labware_type(self) -> Any:
        """Returns the labware type for the labware that contains this location
        Return:
        MessagePropertyInterface: labware type
        """
        return self.labware().properties("labware_type")

    def check_is_location(self) -> bool:
        """Validates that the location provided is a valid location for the labware type
        where this location is defined. It triggers an error if that is not the case.
        Return:
        bool with the result of the validation.
        """
        logger.debug("Location::check_is_location")
        result = False
        if not self.labware_type().validate():
            self.trigger_error(error_codes.ERROR_8_INVALID_LABWARE_TYPE_FOR_LOCATION)
            return False
        if not self._input.validate():
            return False
        if (self._input.value is None) and (len(self.labware_type().valid_locations()) == 0):
            return True
        if not self.check_is_string():
            return False
        result = self.padded() in self.labware_type().valid_locations()
        if not result:
            self.trigger_error(error_codes.ERROR_7_INVALID_LOCATION, text=f"input: {self._input.value}")
        return result

    def unpadded(self) -> Any:
        """It returns the unpadded version of the location
        Eg: If location was 'A01' it would return 'A1'
        """
        if self._input.value is None:
            return None

        text = self._input.value
        if len(text) == 2:
            return text
        if len(text) == 3:
            if text[1] == "0":
                return f"{text[0]}{text[2]}"
            return text

        return text

    def padded(self) -> Any:
        """It returns the padded version of the location
        Eg: If location was 'A1' it would return 'A01'
        """
        if self._input.value is None:
            return None

        text = self._input.value
        if len(text) == 3:
            return text
        if len(text) == 2:
            return f"{text[0]}0{text[1]}"

        return text
