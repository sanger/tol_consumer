import logging
from tol_lab_share.constants.input_bioscan_pool_xp_to_traction_message import (
    SAMPLE_SAMPLE_NAME,
    SAMPLE_SAMPLE_UUID,
    SAMPLE_SPECIES_NAME,
)
from tol_lab_share.messages.properties import MessageProperty
from ..complex.uuid import Uuid
from ..simple.dict_value import DictValue
from ..simple.string_value import StringValue

logger = logging.getLogger(__name__)


class BioscanPoolXpSample(MessageProperty):
    """MessageProperty that handles the parsing of a Bioscan Pool XP tube sample."""

    def __init__(self, input: MessageProperty):
        super().__init__(input)

        self.add_property("name", StringValue(DictValue(input, SAMPLE_SAMPLE_NAME)))
        self.add_property("uuid", Uuid(DictValue(input, SAMPLE_SAMPLE_UUID)))
        self.add_property("species_name", StringValue(DictValue(input, SAMPLE_SPECIES_NAME)))
