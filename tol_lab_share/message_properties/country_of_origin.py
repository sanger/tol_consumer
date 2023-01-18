from .message_property import MessageProperty
from tol_lab_share.config.insdc import COUNTRIES
from tol_lab_share import error_codes
import logging

logger = logging.getLogger(__name__)


class CountryOfOrigin(MessageProperty):
    @property
    def validators(self):
        return [self.check_is_string, self.check_is_valid_country]

    def check_is_valid_country(self):
        logger.debug("CountryOfOrigin::check_is_valid_country")
        if not self._input.validate():
            return False

        result = False
        try:
            result = COUNTRIES.index(self._input.value) >= 0
        except AttributeError:
            pass
        except ValueError:
            pass
        if not result:
            self.add_error(
                error_codes.ERROR_4_NOT_VALID_COUNTRY_INSDC.trigger(
                    instance=self, text=f"input_value: {self._input.value}"
                )
            )
        return result
