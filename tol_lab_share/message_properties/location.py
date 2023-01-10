from .message_property import MessageProperty
from tol_lab_share import error_codes

import logging

logger = logging.getLogger(__name__)


class Location(MessageProperty):
    def __init__(self, labware_type, input):
        super().__init__(input)
        self._labware_type = labware_type

    @property
    def validators(self):
        return [self.check_is_location]

    def check_is_location(self):
        logger.debug("MessageProperty::check_is_location")
        result = False
        if not self._labware_type.validate():
            self.add_error(error_codes.ERROR_8_INVALID_LABWARE_TYPE_FOR_LOCATION)
            return False
        if not self._input.validate():
            return False

        try:
            if (self._input.value is None) and (len(self._labware_type.valid_locations()) == 0):
                return True
            result = self._labware_type.valid_locations().index(self._input.value) >= 0
        except AttributeError:
            pass
        except ValueError:
            pass
        if not result:
            self.add_error(error_codes.ERROR_7_INVALID_LOCATION)
        return result
