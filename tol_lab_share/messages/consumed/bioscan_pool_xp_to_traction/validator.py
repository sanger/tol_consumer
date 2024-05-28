import logging

from tol_lab_share.messages.consumed.base_validator import BaseValidator
from .root import Root

LOGGER = logging.getLogger(__name__)


class Validator(BaseValidator):
    def __init__(self, message: Root):
        self._message = message

    def validate(self) -> bool:
        LOGGER.debug("Starting validation of Bioscan Pool XP to Traction message payload.")

        self._reset_errors()
        self._check_is_uuid(self._message.message_uuid)
        self._check_is_uuid(self._message.request.study_uuid)
        self._check_is_uuid(self._message.sample.uuid)

        LOGGER.debug("Validation finished.")
        return len(self._errors) == 0
