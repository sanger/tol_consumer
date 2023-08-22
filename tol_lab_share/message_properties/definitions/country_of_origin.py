from .message_property import MessageProperty
from tol_lab_share.config.insdc import COUNTRIES
from tol_lab_share import error_codes
import logging
from typing import List, Callable

logger = logging.getLogger(__name__)


class CountryOfOrigin(MessageProperty):
    """MessageProperty subclass to manage parsing of a valid country of origin provided by another
    MessageProperty. The country has to be a country string from the list provided in
    tol_lab_share.config.insdc.
    Eg: 'Australia'
    """

    @property
    def validators(self) -> List[Callable]:
        """Defines the list of validators"""
        return [self.check_is_string, self.check_is_valid_country]

    def check_is_valid_country(self):
        """Given a MessageProperty instance in self._input, it will validate that its value is
        one of the values of the list of countries in tol_lab_share.config.insdc.
        If that is not the case, it will trigger an error (not valid country insdc).
        """
        logger.debug("CountryOfOrigin::check_is_valid_country")
        result = False
        if not self._input.validate():
            return result
        
        if self.check_is_string():
            for country in COUNTRIES:
                if self._input.value.lower() == country.lower():
                    result = True
                    self._input.value = country

        if not result:
            self.trigger_error(error_codes.ERROR_4_NOT_VALID_COUNTRY_INSDC, text=f"input_value: {self._input.value}")
        return result
