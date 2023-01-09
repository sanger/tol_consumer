from .message_property import MessageProperty
from tol_lab_share.message_properties.public_name import PublicName
from tol_lab_share.data_resolvers.data_resolver import DataResolver
from tol_lab_share.messages.output_traction_message import OutputTractionMessage

from tol_lab_share.constants import (
    INPUT_CREATE_LABWARE_MESSAGE_SAMPLE_PUBLIC_NAME,
)

import logging

logger = logging.getLogger(__name__)


class Sample(MessageProperty):
    def __init__(self, input):
        super().__init__(input)
        self._properties = {
            "public_name": DataResolver(PublicName(input[INPUT_CREATE_LABWARE_MESSAGE_SAMPLE_PUBLIC_NAME])),
        }

    def resolve(self):
        logger.debug("Sample::resolve")
        super().resolve()
        output_traction_message = OutputTractionMessage()
        for prop in self._properties_instances:
            prop.add_to_traction_message(output_traction_message)

        if output_traction_message.validate():
            output_traction_message.send()

        self._resolved = output_traction_message.was_sent_correctly()
