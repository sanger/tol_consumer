from typing import Dict, Optional, List
from json import dumps
from requests import post, codes
from tol_lab_share.messages.output_feedback_message import OutputFeedbackMessage

from tol_lab_share import error_codes
from tol_lab_share.error_codes import ErrorCode
from requests.exceptions import JSONDecodeError


class OutputTractionMessageRequest:
    def __init__(self):
        self._library_type = None
        self._study_uuid = None
        self._sample_name = None
        self._sample_uuid = None
        self._container_barcode = None
        self._container_location = None
        self._container_type = None
        self._species = None

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
    # "cost_code": "0000", "data_type": "basecalls"

    def __init__(self, instance: OutputTractionMessageRequest):
        self.instance = instance

    def request_payload(self):
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


class OutputTractionMessage:
    def __init__(self):
        self._requests: Dict[int, OutputTractionMessageRequest] = {}
        self._errors: List[ErrorCode] = []
        self._sent = False

    def requests(self, position: int) -> OutputTractionMessageRequest:
        if position not in self._requests:
            self._requests[position] = OutputTractionMessageRequest()

        return self._requests[position]

    def request_attributes(self):
        return [self.requests(position).serializer().payload() for position in range(len(self._requests))]

    @property
    def errors(self):
        return self._errors

    def payload(self):
        return {
            "data": {
                "type": "receptions",
                "attributes": {"source": "traction-ui.sequencescape", "request_attributes": self.request_attributes()},
            }
        }

    def validate(self):
        return len(self._errors) == 0

    def error_code_traction_problem(self, status_code, error_str):
        return error_codes.ERROR_13_TRACTION_REQUEST_FAILED.with_description(
            f"HTTP CODE: { status_code }, MSG: {error_str}"
        )

    def send(self, url):
        headers = {"Content-type": "application/vnd.api+json", "Accept": "application/vnd.api+json"}

        r = post(url, headers=headers, data=dumps(self.payload()), verify=False)

        self._sent = r.status_code == codes.ok

        if not self._sent:
            try:
                json = r.json()
                self._errors = [
                    self.error_code_traction_problem(r.status_code, error_str) for error_str in json["errors"]
                ]
            except JSONDecodeError:
                self._errors = [self.error_code_traction_problem(r.status_code, r.text)]

        return self._sent

    def add_to_feedback_message(self, feedback_message: OutputFeedbackMessage) -> None:
        if not self._sent:
            feedback_message.operation_was_error_free = False
        if len(self._errors) > 0:
            for error_code in self._errors:
                feedback_message.add_error_code(error_code)
