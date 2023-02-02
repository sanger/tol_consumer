from typing import Optional
from lab_share_lib.rabbit.avro_encoder import AvroEncoderJson, AvroEncoderBinary
from lab_share_lib.constants import RABBITMQ_HEADER_VALUE_ENCODER_TYPE_BINARY, RABBITMQ_HEADER_VALUE_ENCODER_TYPE_JSON
from tol_lab_share.constants import (
    RABBITMQ_SUBJECT_CREATE_LABWARE_FEEDBACK,
    RABBITMQ_ROUTING_KEY_CREATE_LABWARE_FEEDBACK,
)
from tol_lab_share import error_codes
from tol_lab_share.message_properties.definitions.message_property import MessageProperty
from tol_lab_share.messages.interfaces import OutputFeedbackMessageInterface
import logging
from tol_lab_share.helpers import get_config
from tol_lab_share.message_properties.definitions.input import Input
from typing import Dict, Any

from lab_share_lib.rabbit.basic_publisher import BasicPublisher
from lab_share_lib.rabbit.schema_registry import SchemaRegistry

logger = logging.getLogger(__name__)


class OutputFeedbackMessage(MessageProperty, OutputFeedbackMessageInterface):
    """Class that handles the feedback message parsing for TOL lab share"""

    def __init__(self):
        """Constructor that resets the state of a feedback message"""
        super().__init__(Input(self))

        self._source_message_uuid: Optional[bytes] = None
        self._count_of_total_samples: Optional[int] = None
        self._count_of_valid_samples: Optional[int] = None
        self._operation_was_error_free: Optional[bool] = True

    @property
    def validators(self):
        """List of validators to apply to the message"""
        return [self.check_defined_keys, self.check_errors_correct]

    @property
    def origin(self):
        """ "Name of the origin for this property, set as a constant value."""
        return "OutputFeedbackMessage"

    @property
    def source_message_uuid(self) -> Optional[bytes]:
        """Returns the uuid of the source message"""
        return self._source_message_uuid

    @source_message_uuid.setter
    def source_message_uuid(self, value: bytes) -> None:
        """Sets the uuid of the source message"""
        self._source_message_uuid = value

    @property
    def count_of_total_samples(self) -> Optional[int]:
        """Returns the count of total samples"""
        return self._count_of_total_samples

    @count_of_total_samples.setter
    def count_of_total_samples(self, value: int) -> None:
        """Sets the count of total samples"""
        self._count_of_total_samples = value

    @property
    def count_of_valid_samples(self) -> Optional[int]:
        """Returns the count of valid samples"""
        return self._count_of_valid_samples

    @count_of_valid_samples.setter
    def count_of_valid_samples(self, value: int) -> None:
        """Sets the count of valid samples"""
        self._count_of_valid_samples = value

    @property
    def operation_was_error_free(self) -> Optional[bool]:
        """Returns the flag indicating if the operation was error free"""
        return self._operation_was_error_free

    @operation_was_error_free.setter
    def operation_was_error_free(self, value: bool) -> None:
        """Sets the flag indicating if the operation was error free"""
        self._operation_was_error_free = value

    def to_json(self) -> Dict[str, Any]:
        """Returns a Dict with the JSON-like representation of the message."""
        return {
            "sourceMessageUuid": str(self.source_message_uuid),
            "countOfTotalSamples": self.count_of_total_samples,
            "countOfValidSamples": self.count_of_valid_samples,
            "operationWasErrorFree": self.operation_was_error_free,
            "errors": [error.json() for error in self.errors],
        }

    def encoder_config_for(self, encoder_type_selection: str) -> Dict[str, Any]:
        """Returns a config object with the encoder class and encoder type depending of the encoder selected."""
        if encoder_type_selection == "json":
            return {"encoder_class": AvroEncoderJson, "encoder_type": RABBITMQ_HEADER_VALUE_ENCODER_TYPE_JSON}
        else:
            return {"encoder_class": AvroEncoderBinary, "encoder_type": RABBITMQ_HEADER_VALUE_ENCODER_TYPE_BINARY}

    def publish(self, publisher: BasicPublisher, schema_registry: SchemaRegistry, exchange: str) -> None:
        """Publish a new message in the queue with the current contents of the feedback message
        Parameters:
        publisher (BasicPublisher) instance of basic publisher that we will use to connect to rabbitmq
        schema_registry (SchemaRegistry) instance of schema registry that we will use to retrieve data from redpanda
        exchange (str) name of the exchange where we will publish the message in Rabbitmq
        """
        encoder_selected = get_config("").SELECTED_ENCODER_FOR_FEEDBACK_MESSAGE
        encoder_class = self.encoder_config_for(encoder_selected)["encoder_class"]
        encoder_type = self.encoder_config_for(encoder_selected)["encoder_type"]

        encoder = encoder_class(schema_registry, RABBITMQ_SUBJECT_CREATE_LABWARE_FEEDBACK)

        message = self.to_json()
        encoded_message = None
        try:
            encoded_message = encoder.encode([message])
        except BaseException as e:
            self.trigger_error(error_codes.ERROR_22_CANNOT_ENCODE_FEEDBACK_MESSAGE, text=str(e))
            return

        logger.info(f"Sending json: { message }")

        publisher.publish_message(
            exchange,
            RABBITMQ_ROUTING_KEY_CREATE_LABWARE_FEEDBACK,
            encoded_message.body,
            RABBITMQ_SUBJECT_CREATE_LABWARE_FEEDBACK,
            encoded_message.version,
            encoder_type,
        )

    def check_defined_keys(self) -> bool:
        """Checks that the message has defined all required keys, or trigger an error if not"""
        json = self.to_json()
        for key in ["sourceMessageUuid", "countOfTotalSamples", "countOfValidSamples", "operationWasErrorFree"]:
            if json[key] is None:
                self.trigger_error(
                    error_codes.ERROR_15_FEEDBACK_UNDEFINED_KEY,
                    text=f"Key {key} is undefined in feedback message",
                )

                return False
        return True

    def check_errors_correct(self) -> bool:
        """Returns the aggregation result of the validation of all errors content"""
        return all([error.validate() for error in self.errors])
