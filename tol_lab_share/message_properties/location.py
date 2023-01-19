from .message_property import MessageProperty
from tol_lab_share import error_codes

import logging

logger = logging.getLogger(__name__)


class Location(MessageProperty):
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

        try:
            if (self._input.value is None) and (len(self.labware_type().valid_locations()) == 0):
                return True
            result = self.labware_type().valid_locations().index(self._input.value) >= 0
        except AttributeError:
            pass
        except ValueError:
            pass
        if not result:
            self.trigger_error(error_codes.ERROR_7_INVALID_LOCATION, text=f"input: {self._input.value}")
        return result
