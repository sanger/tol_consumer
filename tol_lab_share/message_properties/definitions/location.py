from .message_property import MessageProperty
from tol_lab_share import error_codes
from functools import cached_property

import logging

logger = logging.getLogger(__name__)


class Location(MessageProperty):
    @cached_property
    def value(self):
        if self._input.value is None:
            return None

        return self.unpadded()

    @property
    def validators(self):
        return [self.check_is_location]

    def sample(self):
        return self.property_source

    def labware(self):
        return self.sample().property_source

    def labware_type(self):
        return self.labware().properties("labware_type")

    def check_is_location(self):
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

    def unpadded(self):
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

    def padded(self):
        if self._input.value is None:
            return None

        text = self._input.value
        if len(text) == 3:
            return text
        if len(text) == 2:
            return f"{text[0]}0{text[1]}"

        return text
