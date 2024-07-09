import logging
from typing import Any, Callable

from lab_share_lib.constants import RABBITMQ_HEADER_VALUE_ENCODER_TYPE_JSON, RABBITMQ_HEADER_VALUE_ENCODER_TYPE_BINARY
from lab_share_lib.rabbit.avro_encoder import AvroEncoderJson, AvroEncoderBinary
from lab_share_lib.rabbit.basic_publisher import BasicPublisher

from tol_lab_share import error_codes
from tol_lab_share.error_codes import ErrorCode
from tol_lab_share.helpers import get_config
from tol_lab_share.messages.properties import MessageProperty
from tol_lab_share.messages.properties.simple import Value

logger = logging.getLogger(__name__)


class AliquotMessage:
    """Class that serialises into an aliquot"""

    def __init__(self):
        """Constructor that initializes an aliquot message"""
        self.id_lims: str | None = None
        self.lims_uuid: str | None = None
        self.aliquot_type: str | None = None
        self.source_type: str | None = None
        self.source_barcode: str | None = None
        self.sample_name: str | None = None
        self.used_by_type: str | None = None
        self.used_by_barcode: str | None = None
        self.volume: float | None = None
        self.concentration: float | None = None
        self.insert_size: int | None = None
        self.last_updated: str | None = None
        self.recorded_at: str | None = None
        self.created_at: str | None = None


class WarehouseReceptionMessage(MessageProperty):
    """Class that handles publishing of a volume tracking message to the warehouse"""

    def __init__(self):
        """Reset initial data"""
        super().__init__(Value(self))
        self.lims: str | None = None
        self.aliquot: AliquotMessage | None = None
        self._sent = False
        self._validate_certificates = get_config().CERTIFICATES_VALIDATION_ENABLED

    @property
    def origin(self) -> Any:
        """The origin identifier for this message type.
        This will be appended to any errors generated via the `trigger_error` method.

        Returns:
            str: The origin identifier.
        """
        return "WarehouseReceptionMessage"

    @property
    def validators(self) -> list[Callable]:
        return []

    @property
    def errors(self) -> list[ErrorCode]:
        """A list of errors defined for this message."""
        return self._errors

    def check_no_errors(self) -> bool:
        """Check that the message has no errors.

        Returns:
            bool: True if there are no errors registered; otherwise False.
        """
        return not self.errors

    def to_json(self) -> dict[str, Any]:
        """Returns a dict with the JSON-like representation of the message."""

        return {"lims": self.lims, "aliquot": self.aliquot}

    @staticmethod
    def encoder_config_for(encoder_type_selection: str) -> dict[str, Any]:
        """Returns a config object with the encoder class and encoder type depending of the encoder selected."""
        if encoder_type_selection == "json":
            return {"encoder_class": AvroEncoderJson, "encoder_type": RABBITMQ_HEADER_VALUE_ENCODER_TYPE_JSON}
        else:
            return {"encoder_class": AvroEncoderBinary, "encoder_type": RABBITMQ_HEADER_VALUE_ENCODER_TYPE_BINARY}

    def publish(self, publisher: BasicPublisher, exchange: str) -> None:
        """Publish a new message in the queue with the current contents of the feedback message
        Parameters:
        publisher (BasicPublisher) instance of basic publisher that we will use to connect to rabbitmq
        schema_registry (SchemaRegistry) instance of schema registry that we will use to retrieve data from redpanda
        exchange (str) name of the exchange where we will publish the message in Rabbitmq
        """

        message = self.to_json()

        logger.info(f"Sending json: { message }")

        publisher.publish_message(
            exchange,
            None,
            message,
            None,
            None,
            None,
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
