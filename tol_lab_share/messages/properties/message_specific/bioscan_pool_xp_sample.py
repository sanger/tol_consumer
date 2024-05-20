from functools import singledispatchmethod
import logging
from tol_lab_share.constants.input_bioscan_pool_xp_to_traction_message import (
    SAMPLE_SAMPLE_NAME,
    SAMPLE_SAMPLE_UUID,
    SAMPLE_SPECIES_NAME,
)
from tol_lab_share.messages.properties import MessageProperty
from tol_lab_share.messages.traction.reception_message import TractionReceptionMessageRequest
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

    @singledispatchmethod
    def add_to_message_property(self, message_property: MessageProperty) -> None:
        super().add_to_message_property(message_property)

    @add_to_message_property.register
    def _(self, request: TractionReceptionMessageRequest) -> None:
        """Adds the sample information to a TractionReceptionMessageRequest.

        Args:
            message (TractionReceptionMessageRequest): The Traction request to add the data to.
        """
        super().add_to_message_property(request)

        request.sample_name = self.properties("name").value
        request.sample_uuid = self.properties("uuid").value
        request.species = self.properties("species_name").value
