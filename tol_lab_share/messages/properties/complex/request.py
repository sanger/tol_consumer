from .uuid import Uuid
from tol_lab_share.constants.input_bioscan_pool_xp_to_traction_message import (
    REQUEST_COST_CODE,
    REQUEST_GENOME_SIZE,
    REQUEST_LIBRARY_TYPE,
    REQUEST_STUDY_UUID,
)
from tol_lab_share.messages.properties.simple import DictValue, StringValue
from tol_lab_share.messages.properties import MessageProperty

import logging

logger = logging.getLogger(__name__)


class Request(MessageProperty):
    """MessageProperty that handles the parsing of a request section for TOL messages."""

    def __init__(self, input: MessageProperty):
        super().__init__(input)

        self.add_property("cost_code", StringValue(DictValue(input, REQUEST_COST_CODE)))
        self.add_property(
            "genome_size", StringValue(DictValue(input, REQUEST_GENOME_SIZE, optional=True), optional=True)
        )
        self.add_property("library_type", StringValue(DictValue(input, REQUEST_LIBRARY_TYPE)))
        self.add_property("study_uuid", Uuid(DictValue(input, REQUEST_STUDY_UUID)))
