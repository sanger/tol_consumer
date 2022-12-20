from .message_property import MessageProperty
from tol_lab_share.message_properties.public_name import PublicName
from tol_lab_share.data_resolvers.data_resolver import DataResolver

from tol_lab_share.constants import (
    INPUT_CREATE_LABWARE_MESSAGE_SAMPLE_PUBLIC_NAME,
)


class Sample(MessageProperty):
    def __init__(self, input):
        super().__init__(input)
        self._properties = {
            "public_name": DataResolver(PublicName(input[INPUT_CREATE_LABWARE_MESSAGE_SAMPLE_PUBLIC_NAME])),
        }
