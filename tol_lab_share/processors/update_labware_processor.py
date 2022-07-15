# mypy: allow-untyped-defs
from lab_share_lib.rabbit.avro_encoder import AvroEncoder  # type: ignore
import logging

from tol_lab_share.constants import (
    RABBITMQ_SUBJECT_UPDATE_LABWARE_FEEDBACK,
    RABBITMQ_ROUTING_KEY_UPDATE_LABWARE_FEEDBACK,
)

from lab_share_lib.processing.rabbit_message import RabbitMessage  # type: ignore

logger = logging.getLogger(__name__)


class UpdateLabwareProcessor:
    def __init__(self, schema_registry, basic_publisher, config):
        logger.debug("UpdateLabwareProcessor::__init__")
        self._encoder = AvroEncoder(schema_registry, RABBITMQ_SUBJECT_UPDATE_LABWARE_FEEDBACK)
        self._basic_publisher = basic_publisher
        self._config = config

    def process(self, message: RabbitMessage) -> bool:
        logger.debug("UpdateLabwareProcessor::process")
        barcode = message.message["barcode"]
        encoded_message = self._encoder.encode([{"success": f"ok update for barcode: { barcode }"}])
        self._basic_publisher.publish_message(
            self._config.RABBITMQ_FEEDBACK_EXCHANGE,
            RABBITMQ_ROUTING_KEY_UPDATE_LABWARE_FEEDBACK,
            encoded_message.body,
            RABBITMQ_SUBJECT_UPDATE_LABWARE_FEEDBACK,
            encoded_message.version,
        )
        return True
