import logging
from typing import Any

from lab_share_lib.processing.base_processor import BaseProcessor
from lab_share_lib.processing.rabbit_message import RabbitMessage
from lab_share_lib.rabbit.basic_publisher import BasicPublisher
from lab_share_lib.rabbit.schema_registry import SchemaRegistry
from tol_lab_share.messages.consumed import TractionToWarehouseMessage
from tol_lab_share.messages.mappers.traction_to_warehouse import TractionToWarehouseMapper

from tol_lab_share.messages.mlwh.create_aliquot_message import CreateAliquotInWarehouseMessage

logger = logging.getLogger(__name__)


class CreateAliquotProcessor(BaseProcessor):
    """Class to handle consuming create-aliquot messages from TOL"""

    def __init__(self, schema_registry: SchemaRegistry, basic_publisher: BasicPublisher, config: Any):
        """Resets data for the processor
        Parameters:
        schema_registry (SchemaRegistry) the redpanda schema registry we will us to validate messages
        basic_publisher (BasicPublisher) instance that will provide the communication with the queues system
        config (Any) mainconfiguration from the app
        """
        logger.debug("CreateAliquotProcessor::__init__")

        self._basic_publisher = basic_publisher
        self._schema_registry = schema_registry
        self._config = config

    @staticmethod
    def instantiate(
        schema_registry: SchemaRegistry, basic_publisher: BasicPublisher, config: Any
    ) -> "CreateAliquotProcessor":
        """Instantiate a CreateAliquotProcessor"""
        return CreateAliquotProcessor(schema_registry, basic_publisher, config)

    def process(self, emq_message: RabbitMessage) -> bool:
        """
        1. Receives a message from rabbitmq.
        2. Validates the message with RedPanda schema.
        3. Push messages to the warehouse RMQ.
        """
        logger.debug("CreateAliquotProcessor::process")
        logger.info(f"Message received: {emq_message}")

        input_message_from_traction = TractionToWarehouseMessage(emq_message.message)
        output_warehouse_message = CreateAliquotInWarehouseMessage()

        TractionToWarehouseMapper.map(input_message_from_traction, output_warehouse_message)
        logger.info("Attempting to send the message to the warehouse.")
        output_warehouse_message.publish(self._basic_publisher, "psd.tol-lab-share")

        logger.info("Message processing completed.")
        return True
