from .message_property import MessageProperty
from requests import get, codes
from functools import cached_property
from tol_lab_share.helpers import get_config
from tol_lab_share import error_codes
from typing import Any, Dict, cast
from typing import List, Callable

CACHE_TAXON_IDS: Dict[str, str] = {}
MAX_CACHE_SIZE = 1000


class ScientificNameFromTaxonId(MessageProperty):
    """MessageProperty subclass to manage resolving the scientific name that
    represents the taxon id received as input.
    """

    @property
    def validators(self) -> List[Callable]:
        """Checks the input is a integer string"""
        return [self.check_is_integer_string]

    @cached_property
    def taxonomy_url(self) -> str:
        """URL with the reference to the EBI taxonomy service that resolves
        taxon ids into scientific names."""
        return cast(str, get_config("").EBI_TAXONOMY_URL)

    @cached_property
    def value(self) -> Any:
        """Resolves the value of the scientific name by querying the EBI service
        for the value given to the taxon id stored in current instance. It also
        caches the value so it can be reused by other objects.
        It also performs a very simple cache size releasing to avoid memory leaking.
        """
        if self._input.value not in CACHE_TAXON_IDS:
            if len(CACHE_TAXON_IDS) > MAX_CACHE_SIZE:
                ScientificNameFromTaxonId.reset_cache()

            r = get(f"{ self.taxonomy_url }/{ self._input.value }")

            self._success = r.status_code == codes.ok

            if self._success:
                json = r.json()
                CACHE_TAXON_IDS[self._input.value] = json["scientificName"]
            else:
                self.trigger_error(
                    error_codes.ERROR_14_PROBLEM_ACCESSING_TAXON_ID,
                    text=f"HTTP code {r.status_code} - Problem when accessing taxon id {self._input.value}",
                )

        return CACHE_TAXON_IDS[self._input.value]

    @staticmethod
    def reset_cache():
        """Static method to reset the cache shared by all instances"""
        CACHE_TAXON_IDS.clear()
