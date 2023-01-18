from typing import List, Optional
from lab_share_lib.rabbit.avro_encoder import AvroEncoderJson, AvroEncoderBinary
from lab_share_lib.constants import RABBITMQ_HEADER_VALUE_ENCODER_TYPE_BINARY, RABBITMQ_HEADER_VALUE_ENCODER_TYPE_JSON
from tol_lab_share.constants import (
    RABBITMQ_SUBJECT_CREATE_LABWARE_FEEDBACK,
    RABBITMQ_ROUTING_KEY_CREATE_LABWARE_FEEDBACK,
)
from tol_lab_share import error_codes
from tol_lab_share.messages.message import Message
import logging
from tol_lab_share.helpers import get_config

logger = logging.getLogger(__name__)


class OutputFeedbackMessage(Message):
    @property
    def validators(self):
        return [self.check_defined_keys, self.check_errors_correct]

    def __init__(self):
        self._source_message_uuid: Optional[bytes] = None
        self._count_of_total_samples: Optional[int] = None
        self._count_of_valid_samples: Optional[int] = None
        self._operation_was_error_free: Optional[bool] = True
        self._errors: List[List[str]] = []

    @property
    def source_message_uuid(self) -> Optional[bytes]:
        return self._source_message_uuid

    @source_message_uuid.setter
    def source_message_uuid(self, value: bytes) -> None:
        self._source_message_uuid = value

    @property
    def count_of_total_samples(self) -> Optional[int]:
        return self._count_of_total_samples

    @count_of_total_samples.setter
    def count_of_total_samples(self, value: int) -> None:
        self._count_of_total_samples = value

    @property
    def count_of_valid_samples(self) -> Optional[int]:
        return self._count_of_valid_samples

    @count_of_valid_samples.setter
    def count_of_valid_samples(self, value: int) -> None:
        self._count_of_valid_samples = value

    @property
    def operation_was_error_free(self) -> Optional[bool]:
        return self._operation_was_error_free

    @operation_was_error_free.setter
    def operation_was_error_free(self, value: bool) -> None:
        self._operation_was_error_free = value

    def to_json(self):
        return {
            "sourceMessageUuid": self.source_message_uuid,
            "countOfTotalSamples": self.count_of_total_samples,
            "countOfValidSamples": self.count_of_valid_samples,
            "operationWasErrorFree": self.operation_was_error_free,
            "errors": [error.json() for error in self.errors],
        }

    def encoder_config_for(self, encoder_type_selection):
        if encoder_type_selection == "json":
            return {"encoder_class": AvroEncoderJson, "encoder_type": RABBITMQ_HEADER_VALUE_ENCODER_TYPE_JSON}
        else:
            return {"encoder_class": AvroEncoderBinary, "encoder_type": RABBITMQ_HEADER_VALUE_ENCODER_TYPE_BINARY}

    def publish(self, publisher, schema_registry, exchange):
        encoder_selected = get_config("").SELECTED_ENCODER_FOR_FEEDBACK_MESSAGE
        encoder_class = self.encoder_config_for(encoder_selected)["encoder_class"]
        encoder_type = self.encoder_config_for(encoder_selected)["encoder_type"]

        encoder = encoder_class(schema_registry, RABBITMQ_SUBJECT_CREATE_LABWARE_FEEDBACK)

        message = self.to_json()
        encoded_message = encoder.encode([message])

        logger.debug(f"Sending: { encoded_message }")

        publisher.publish_message(
            exchange,
            RABBITMQ_ROUTING_KEY_CREATE_LABWARE_FEEDBACK,
            encoded_message.body,
            RABBITMQ_SUBJECT_CREATE_LABWARE_FEEDBACK,
            encoded_message.version,
            encoder_type,
        )

    def check_defined_keys(self):
        json = self.to_json()
        for key in ["sourceMessageUuid", "countOfTotalSamples", "countOfValidSamples", "operationWasErrorFree"]:
            if json[key] is None:
                self.add_error_code(
                    error_codes.ERROR_15_FEEDBACK_UNDEFINED_KEY.trigger(
                        text=f"Key {key} is undefined in feedback message", instance=self
                    )
                )
                return False
        return True

    def check_errors_correct(self):
        return all([error.validate() for error in self.errors])
