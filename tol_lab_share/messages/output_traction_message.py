from typing import Dict, Optional
from json import dumps
from requests import post, codes
from tol_lab_share.messages.interfaces import (
    OutputTractionMessageInterface,
    OutputFeedbackMessageInterface,
    OutputTractionMessageRequestInterface,
)
from tol_lab_share.message_properties.definitions.message_property import MessageProperty
from tol_lab_share.message_properties.definitions.input import Input
from tol_lab_share.constants import (
    OUTPUT_TRACTION_MESSAGE_CREATE_REQUEST_CONTAINER_TYPE_WELLS,
    OUTPUT_TRACTION_MESSAGE_CREATE_REQUEST_CONTAINER_TYPE_TUBES,
)
from tol_lab_share import error_codes


class OutputTractionMessageRequest(OutputTractionMessageRequestInterface):
    def __init__(self):
        self._library_type = None
        self._study_uuid = None
        self._sample_name = None
        self._sample_uuid = None
        self._container_barcode = None
        self._container_location = None
        self._container_type = None
        self._species = None

    def validate(self) -> bool:
        return (
            (self._library_type is not None)
            and (self._study_uuid is not None)
            and (self._sample_name is not None)
            and (self._container_barcode is not None)
            and (self._species is not None)
            and (
                (self._container_type == OUTPUT_TRACTION_MESSAGE_CREATE_REQUEST_CONTAINER_TYPE_WELLS)
                or (self._container_type == OUTPUT_TRACTION_MESSAGE_CREATE_REQUEST_CONTAINER_TYPE_TUBES)
            )
            and (self._species is not None)
        )

    @property
    def species(self) -> Optional[str]:
        return self._species

    @species.setter
    def species(self, value: Optional[str]) -> None:
        self._species = value

    @property
    def container_type(self) -> Optional[str]:
        return self._container_type

    @container_type.setter
    def container_type(self, value: Optional[str]) -> None:
        self._container_type = value

    @property
    def container_location(self) -> Optional[str]:
        return self._container_location

    @container_location.setter
    def container_location(self, value: Optional[str]) -> None:
        self._container_location = value

    @property
    def container_barcode(self) -> Optional[str]:
        return self._container_barcode

    @container_barcode.setter
    def container_barcode(self, value: Optional[str]) -> None:
        self._container_barcode = value

    @property
    def sample_uuid(self) -> Optional[str]:
        return self._sample_uuid

    @sample_uuid.setter
    def sample_uuid(self, value: Optional[str]) -> None:
        self._sample_uuid = value

    @property
    def sample_name(self) -> Optional[str]:
        return self._sample_name

    @sample_name.setter
    def sample_name(self, value: Optional[str]) -> None:
        self._sample_name = value

    @property
    def library_type(self) -> Optional[str]:
        return self._library_type

    @library_type.setter
    def library_type(self, value: Optional[str]) -> None:
        self._library_type = value

    @property
    def study_uuid(self) -> Optional[str]:
        return self._study_uuid

    @study_uuid.setter
    def study_uuid(self, value: Optional[str]) -> None:
        self._study_uuid = value

    def serializer(self):
        return RequestSerializer(self)


class RequestSerializer:
    def __init__(self, instance: OutputTractionMessageRequest):
        self.instance = instance

    def is_ont_library_type(self):
        return self.instance.library_type and ("ONT" in self.instance.library_type)

    def request_payload(self):
        if self.is_ont_library_type():
            return {
                "data_type": "basecalls",
                "cost_code": "0000",
                "library_type": self.instance.library_type,
                "external_study_id": self.instance.study_uuid,
            }
        else:
            return {"library_type": self.instance.library_type, "external_study_id": self.instance.study_uuid}

    def sample_payload(self):
        return {
            "name": self.instance.sample_name,
            "external_id": self.instance.sample_uuid,
            "species": self.instance.species,
        }

    def container_payload(self):
        if self.instance.container_type == "tubes":
            return {"type": self.instance.container_type, "barcode": self.instance.container_barcode}
        else:
            return {
                "type": self.instance.container_type,
                "barcode": self.instance.container_barcode,
                "position": self.instance.container_location,
            }

    def payload(self):
        return {
            "request": self.request_payload(),
            "sample": self.sample_payload(),
            "container": self.container_payload(),
        }


class OutputTractionMessage(MessageProperty, OutputTractionMessageInterface):
    def __init__(self):
        super().__init__(Input(self))
        self._requests: Dict[int, OutputTractionMessageRequest] = {}
        self._sent = False

    @property
    def origin(self):
        return "OutputFeedbackMessage"

    @property
    def validators(self):
        return [self.check_has_requests, self.check_requests_have_all_content, self.check_no_errors]

    def requests(self, position: int) -> OutputTractionMessageRequestInterface:
        if position not in self._requests:
            self._requests[position] = OutputTractionMessageRequest()

        return self._requests[position]

    def request_attributes(self):
        return [self._requests[position].serializer().payload() for position in range(len(self._requests))]

    @property
    def errors(self):
        return self._errors

    def check_has_requests(self):
        if len(self._requests) > 0:
            return True
        else:
            self.trigger_error(error_codes.ERROR_23_TRACTION_MESSAGE_HAS_NO_REQUESTS)

    def check_no_errors(self):
        return len(self.errors) == 0

    def check_requests_have_all_content(self):
        if all([self.requests(key).validate() for key in self._requests]):
            return True
        else:
            self.trigger_error(error_codes.ERROR_24_TRACTION_MESSAGE_REQUESTS_HAVE_MISSING_DATA)

    def payload(self):
        return {
            "data": {
                "type": "receptions",
                "attributes": {"source": "traction-ui.sequencescape", "request_attributes": self.request_attributes()},
            }
        }

    def error_code_traction_problem(self, status_code, error_str):
        return self.trigger_error(
            error_codes.ERROR_13_TRACTION_REQUEST_FAILED, text=f"HTTP CODE: { status_code }, MSG: {error_str}"
        )

    def send(self, url):
        headers = {"Content-type": "application/vnd.api+json", "Accept": "application/vnd.api+json"}

        r = post(url, headers=headers, data=dumps(self.payload()), verify=False)

        self._sent = r.status_code == codes.created
        if not self._sent:
            # problem = (r.text[:75] + '..') if len(r.text) > 75 else r.text
            problem = r.text
            self.error_code_traction_problem(r.status_code, problem)

        return self._sent

    def add_to_feedback_message(self, feedback_message: OutputFeedbackMessageInterface) -> None:
        if not self._sent:
            feedback_message.operation_was_error_free = False
        if len(self._errors) > 0:
            for error_code in self._errors:
                feedback_message.add_error(error_code)
