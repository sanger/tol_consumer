from lab_share_lib.rabbit.avro_encoder import AvroEncoder
import logging

from tol_lab_share.constants import RABBITMQ_SUBJECT_UPDATE_LABWARE_FEEDBACK, RABBITMQ_ROUTING_KEY_UPDATE_LABWARE_FEEDBACK
logger = logging.getLogger(__name__)

class UpdateLabwareProcessor:
    def __init__(self, schema_registry, basic_publisher, config):
        logger.debug("UpdateLabwareProcessor::__init__")
        self._encoder = AvroEncoder(schema_registry, RABBITMQ_SUBJECT_UPDATE_LABWARE_FEEDBACK)
        self._basic_publisher = basic_publisher
        self._config = config

    def process(self, message) -> bool:
        logger.debug("UpdateLabwareProcessor::process")
        encoded_message = self._encoder.encode([{"success": "ok"}])
        self._basic_publisher.publish_message(
            self._config.RABBITMQ_FEEDBACK_EXCHANGE,
            RABBITMQ_ROUTING_KEY_UPDATE_LABWARE_FEEDBACK,
            encoded_message.body,
            RABBITMQ_SUBJECT_UPDATE_LABWARE_FEEDBACK,
            encoded_message.version,
        )        
        return True
