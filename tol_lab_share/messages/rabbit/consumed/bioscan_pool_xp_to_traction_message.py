from lab_share_lib.processing.rabbit_message import RabbitMessage
from tol_lab_share.constants.input_bioscan_pool_xp_to_traction_message import (
    MESSAGE_UUID,
    CREATED_DATE_UTC,
    TUBE_BARCODE,
    LIBRARY,
    REQUEST,
    SAMPLE,
)
from tol_lab_share.messages.properties import MessageProperty
from tol_lab_share.messages.properties.complex import DateUtc, Library, MessageUuid, Request
from tol_lab_share.messages.properties.simple import DictValue, StringValue
from tol_lab_share.messages.properties.message_specific import BioscanPoolXpSample

import logging

logger = logging.getLogger(__name__)


class BioscanPoolXpToTractionMessage(MessageProperty):
    """Class that handles parsing a TOL lab share message received"""

    def __init__(self, m: RabbitMessage):
        """Constructor that receives a RabbitMessage and parses it using the properties defined.

        Args:
            m (RabbitMessage): The message to parse.
        """
        super().__init__(m)
        self._message = m.message

        self.add_property("message_uuid", MessageUuid(DictValue(self._message, MESSAGE_UUID)))
        self.add_property("create_date_utc", DateUtc(DictValue(self._message, CREATED_DATE_UTC)))
        self.add_property("tube_barcode", StringValue(DictValue(self._message, TUBE_BARCODE)))
        self.add_property("library", Library(DictValue(self._message, LIBRARY)))
        self.add_property("request", Request(DictValue(self._message, REQUEST)))
        self.add_property("sample", BioscanPoolXpSample(DictValue(self._message, SAMPLE)))
