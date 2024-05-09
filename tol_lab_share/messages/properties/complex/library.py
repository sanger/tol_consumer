from tol_lab_share.constants.input_bioscan_pool_xp_to_traction_message import (
    LIBRARY_VOLUME,
    LIBRARY_CONCENTRATION,
    LIBRARY_BOX_BARCODE,
    LIBRARY_INSERT_SIZE,
)
from tol_lab_share.messages.properties.simple import DictValue, StringValue, Value
from tol_lab_share.messages.traction import TractionReceptionMessage

from tol_lab_share.messages.properties import MessageProperty
from functools import singledispatchmethod

import logging

logger = logging.getLogger(__name__)


class Library(MessageProperty):
    """MessageProperty that handles the parsing of a library for TOL messages."""

    def __init__(self, input: MessageProperty):
        super().__init__(input)

        self.add_property("volume", Value(DictValue(input, LIBRARY_VOLUME)))
        self.add_property("concentration", Value(DictValue(input, LIBRARY_CONCENTRATION)))
        self.add_property("box_barcode", StringValue(DictValue(input, LIBRARY_BOX_BARCODE)))
        self.add_property("insert_size", Value(DictValue(input, LIBRARY_INSERT_SIZE)))

    @singledispatchmethod
    def add_to_message_property(self, message_property: MessageProperty) -> None:
        super().add_to_message_property(message_property)

    @add_to_message_property.register
    def _(self, message: TractionReceptionMessage) -> None:
        """Adds the library information to an OutputTractionMessage.

        Args:
            message (TractionReceptionMessage): The Traction reception message to add the data to.
        """
        super().add_to_message_property(message)
