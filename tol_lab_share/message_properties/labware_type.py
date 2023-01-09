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
