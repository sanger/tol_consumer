from tol_lab_share.constants.input_bioscan_pool_xp_to_traction_message import (
    LIBRARY_VOLUME,
    LIBRARY_CONCENTRATION,
    LIBRARY_BOX_BARCODE,
    LIBRARY_INSERT_SIZE,
)
from tol_lab_share.messages.properties.simple import DictValue, StringValue, FloatValue, IntValue

from tol_lab_share.messages.properties import MessageProperty

import logging

logger = logging.getLogger(__name__)


class Library(MessageProperty):
    """MessageProperty that handles the parsing of a library for TOL messages."""

    def __init__(self, input: MessageProperty):
        super().__init__(input)

        self.add_property("volume", FloatValue(DictValue(input, LIBRARY_VOLUME)))
        self.add_property("concentration", FloatValue(DictValue(input, LIBRARY_CONCENTRATION)))
        self.add_property("box_barcode", StringValue(DictValue(input, LIBRARY_BOX_BARCODE)))
        self.add_property("insert_size", IntValue(DictValue(input, LIBRARY_INSERT_SIZE, optional=True), optional=True))
