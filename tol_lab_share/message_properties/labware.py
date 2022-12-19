from .message_property import MessageProperty
from tol_lab_share.message_properties.labware_type import LabwareType
from tol_lab_share.message_properties.barcode import Barcode
from tol_lab_share.message_properties.sample import Sample
from tol_lab_share.state_machines.data_resolver import DataResolver

from tol_lab_share.constants import (
    INPUT_CREATE_LABWARE_MESSAGE_LABWARE_TYPE,
    INPUT_CREATE_LABWARE_MESSAGE_BARCODE,
    INPUT_CREATE_LABWARE_MESSAGE_SAMPLES,
)


class Labware(MessageProperty):
    def __init__(self, input):
        super().__init__(input)
        self._properties = {
            "labware_type": DataResolver(LabwareType(input[INPUT_CREATE_LABWARE_MESSAGE_LABWARE_TYPE])),
            "barcode": DataResolver(Barcode(input[INPUT_CREATE_LABWARE_MESSAGE_BARCODE])),
            "samples": [DataResolver(Sample(sample)) for sample in input[INPUT_CREATE_LABWARE_MESSAGE_SAMPLES]],
        }
