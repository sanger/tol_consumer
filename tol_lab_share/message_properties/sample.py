from .message_property import MessageProperty
from tol_lab_share.message_properties.public_name import PublicName
from tol_lab_share.message_properties.common_name import CommonName
from tol_lab_share.message_properties.concentration import Concentration
from tol_lab_share.message_properties.country_of_origin import CountryOfOrigin
from tol_lab_share.message_properties.donor_id import DonorId
from tol_lab_share.message_properties.library_type import LibraryType
from tol_lab_share.message_properties.location import Location
from tol_lab_share.message_properties.sanger_sample_id import SangerSampleId
from tol_lab_share.message_properties.taxon_id import TaxonId
from tol_lab_share.message_properties.uuid import Uuid
from tol_lab_share.message_properties.dict_input import DictInput

from tol_lab_share.data_resolvers.data_resolver import DataResolver
from tol_lab_share.messages.output_traction_message import OutputTractionMessage

from tol_lab_share.constants import (
    INPUT_CREATE_LABWARE_MESSAGE_SAMPLE_PUBLIC_NAME,
    INPUT_CREATE_LABWARE_MESSAGE_SAMPLE_COMMON_NAME,
    INPUT_CREATE_LABWARE_MESSAGE_SAMPLE_CONCENTRATION,
    INPUT_CREATE_LABWARE_MESSAGE_SAMPLE_COUNTRY_OF_ORIGIN,
    INPUT_CREATE_LABWARE_MESSAGE_SAMPLE_DONOR_ID,
    INPUT_CREATE_LABWARE_MESSAGE_SAMPLE_LIBRARY_TYPE,
    INPUT_CREATE_LABWARE_MESSAGE_SAMPLE_LOCATION,
    INPUT_CREATE_LABWARE_MESSAGE_SAMPLE_SANGER_SAMPLE_ID,
    INPUT_CREATE_LABWARE_MESSAGE_SAMPLE_SANGER_TAXON_ID,
    INPUT_CREATE_LABWARE_MESSAGE_SAMPLE_SANGER_UUID,
)

import logging

logger = logging.getLogger(__name__)


class Sample(MessageProperty):
    def __init__(self, labware_type, input):
        super().__init__(input)
        self._properties = {
            "common_name": DataResolver(CommonName(DictInput(input, INPUT_CREATE_LABWARE_MESSAGE_SAMPLE_COMMON_NAME))),
            "concentration": DataResolver(
                Concentration(DictInput(input, INPUT_CREATE_LABWARE_MESSAGE_SAMPLE_CONCENTRATION))
            ),
            "country_of_origin": DataResolver(
                CountryOfOrigin(DictInput(input, INPUT_CREATE_LABWARE_MESSAGE_SAMPLE_COUNTRY_OF_ORIGIN))
            ),
            "donor_id": DataResolver(DonorId(DictInput(input, INPUT_CREATE_LABWARE_MESSAGE_SAMPLE_DONOR_ID))),
            "library_type": DataResolver(
                LibraryType(DictInput(input, INPUT_CREATE_LABWARE_MESSAGE_SAMPLE_LIBRARY_TYPE))
            ),
            "location": DataResolver(
                Location(labware_type, DictInput(input, INPUT_CREATE_LABWARE_MESSAGE_SAMPLE_LOCATION))
            ),
            "public_name": DataResolver(PublicName(DictInput(input, INPUT_CREATE_LABWARE_MESSAGE_SAMPLE_PUBLIC_NAME))),
            "sanger_sample_id": DataResolver(
                SangerSampleId(DictInput(input, INPUT_CREATE_LABWARE_MESSAGE_SAMPLE_SANGER_SAMPLE_ID))
            ),
            "taxon_id": DataResolver(TaxonId(DictInput(input, INPUT_CREATE_LABWARE_MESSAGE_SAMPLE_SANGER_TAXON_ID))),
            "uuid": DataResolver(Uuid(DictInput(input, INPUT_CREATE_LABWARE_MESSAGE_SAMPLE_SANGER_UUID))),
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
