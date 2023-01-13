from .message_property import MessageProperty
from requests import get, codes
from functools import cached_property
from lab_share_lib.config_readers import get_config
from tol_lab_share import error_codes

CACHE_TAXON_IDS = {}


class TaxonId(MessageProperty):
    @property
    def validators(self):
        return [self.check_is_integer]

    @cached_property
    def taxonomy_url(self):
        return get_config("")[0].EBI_TAXONOMY_URL

    @cached_property
    def value(self):
        if self._input.value not in CACHE_TAXON_IDS:
            r = get(f"{ self.taxonomy_url }/{ self._input.value }")

            self._success = r.status_code == codes.ok

            if self._success:
                json = r.json()
                CACHE_TAXON_IDS[self._input.value] = json["scientificName"]
            else:
                self.raise_exception(
                    error_codes.ERROR_14_PROBLEM_ACCESSING_TAXON_ID.with_description(
                        f"HTTP code {r.status_code} - Problem when accessing taxon id {self._input.value}"
                    )
                )

        return CACHE_TAXON_IDS[self._input.value]

    @staticmethod
    def reset_cache():
        CACHE_TAXON_IDS.clear()
