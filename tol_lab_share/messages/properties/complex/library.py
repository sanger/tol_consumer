from functools import singledispatchmethod
from tol_lab_share.constants.input_bioscan_pool_xp_to_traction_message import (
    LIBRARY_VOLUME,
    LIBRARY_CONCENTRATION,
    LIBRARY_BOX_BARCODE,
    LIBRARY_INSERT_SIZE,
)
from tol_lab_share.messages.properties.simple import DictValue, StringValue, FloatValue, IntValue

from tol_lab_share.messages.properties import MessageProperty

import logging

from tol_lab_share.messages.traction.reception_message import TractionReceptionMessageRequest

logger = logging.getLogger(__name__)


class Library(MessageProperty):
    """MessageProperty that handles the parsing of a library for TOL messages."""

    def __init__(self, input: MessageProperty):
        super().__init__(input)

        self.add_property("volume", FloatValue(DictValue(input, LIBRARY_VOLUME)))
        self.add_property("concentration", FloatValue(DictValue(input, LIBRARY_CONCENTRATION)))
        self.add_property("box_barcode", StringValue(DictValue(input, LIBRARY_BOX_BARCODE)))
        self.add_property("insert_size", IntValue(DictValue(input, LIBRARY_INSERT_SIZE, optional=True), optional=True))

    @singledispatchmethod
    def add_to_message_property(self, message_property: MessageProperty) -> None:
        super().add_to_message_property(message_property)

    @add_to_message_property.register
    def _(self, request: TractionReceptionMessageRequest) -> None:
        """Adds the library information to a TractionReceptionMessageRequest.

        Args:
            message (TractionReceptionMessageRequest): The Traction request to add the data to.
        """
        super().add_to_message_property(request)

        request.library_volume = self.properties("volume").value
        request.library_concentration = self.properties("concentration").value
        request.template_prep_kit_box_barcode = self.properties("box_barcode").value
        request.library_insert_size = self.properties("insert_size").value
