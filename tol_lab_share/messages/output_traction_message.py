from functools import singledispatchmethod
from typing import Callable, Any
from json import dumps
from datetime import datetime
from requests import post, codes
from tol_lab_share.message_properties.definitions.message_property import MessageProperty
from tol_lab_share.message_properties.definitions.input import Input
from tol_lab_share.constants import (
    OUTPUT_TRACTION_MESSAGE_CONTAINER_TYPES,
    OUTPUT_TRACTION_MESSAGE_SOURCE,
)
from tol_lab_share import error_codes
from tol_lab_share.error_codes import ErrorCode
from tol_lab_share.helpers import get_config
from tol_lab_share.messages.output_feedback_message import OutputFeedbackMessage


class OutputTractionMessageRequest:
    """Class that manages the information of a single Traction request instance as part of the Traction message."""

    def __init__(self):
        """Constructor that initializes all info for a single request."""
        self.accession_number: str | None = None
        self.container_barcode: str | None = None
        self.container_location: str | None = None
        self.container_type: OUTPUT_TRACTION_MESSAGE_CONTAINER_TYPES | None = None
        self.cost_code: str | None = None
        self.country_of_origin: str | None = None
        self.date_of_sample_collection: datetime | None = None
        self.donor_id: str | None = None
        self.library_type: str | None = None
        self.priority_level: str | None = None
        self.public_name: str | None = None
        self.sample_name: str | None = None
        self.sample_uuid: str | None = None
        self.sanger_sample_id: str | None = None
        self.species: str | None = None
        self.study_uuid: str | None = None
        self.supplier_name: str | None = None
        self.taxon_id: str | None = None

    def validate(self) -> bool:
        """Validate the information in this request.

        Returns:
            bool: True if the request is valid; otherwise False.
        """
        return (
            (self.library_type is not None)
            and (self.study_uuid is not None)
            and (self.sample_name is not None)
            and (self.container_barcode is not None)
            and (self.species is not None)
            and (self.container_type is not None)
            and (self.species is not None)
        )


class Serializer:
    """Class to manage the serialization to JSON of the request received as argument in the constructor."""
    @staticmethod
    def request_payload(request: OutputTractionMessageRequest) -> dict[str, Any]:
        """Generate the request payload for the given request.
        The payload varies depending on whether the library type is ONT or not.

        Args:
            request (OutputTractionMessageRequest): The request to generate the payload for.

        Returns:
            dict[str, Any]: A dictionary containing the Traction "request" payload for the request.
        """
        is_ont = request.library_type and ("ONT" in request.library_type)
        if is_ont:
            return {
                "data_type": "basecalls",
                "library_type": request.library_type,
                "external_study_id": request.study_uuid,
                "cost_code": request.cost_code,
            }
        else:
            return {
                "library_type": request.library_type,
                "external_study_id": request.study_uuid,
                "cost_code": request.cost_code,
            }

    @staticmethod
    def sample_payload(request: OutputTractionMessageRequest) -> dict[str, Any]:
        """Generate the sample payload for the given request.

        Args:
            request (OutputTractionMessageRequest): The request to generate the payload for.

        Returns:
            dict[str, Any]: A dictionary containing the Traction "sample" payload for the request.
        """
        collection_date = None
        if request.date_of_sample_collection is not None:
            collection_date = request.date_of_sample_collection.strftime("%Y-%m-%d")

        return {
            "name": request.sample_name,
            "external_id": request.sample_uuid,
            "species": request.species,
            "priority_level": request.priority_level,
            "sanger_sample_id": request.sanger_sample_id,
            "supplier_name": request.supplier_name,
            "public_name": request.public_name,
            "taxon_id": request.taxon_id,
            "donor_id": request.donor_id,
            "country_of_origin": request.country_of_origin,
            "accession_number": request.accession_number,
            "date_of_sample_collection": collection_date,
        }


class PlateSerializer(Serializer):
    """Class to manage the serialization of plate requests."""

    def __init__(self, plate_requests: list[OutputTractionMessageRequest]):
        """Constructor.

        Args:
            plate_requests (list[OutputTractionMessageRequest]): The list of requests to serialize for a single plate.
        """
        self._requests = plate_requests

    def payload(self) -> dict[str, Any]:
        """Generate a payload with the information required by Traction.

        Returns:
            dict[str, Any]: A dictionary containing the overall payload.
        """
        return {
            "request": self.request_payload(self._requests[0]),
            "sample": self.sample_payload(self._requests[0]),
        }

class TubeSerializer(Serializer):
    """Class to manage the serialization of plate requests."""

    def __init__(self, tube_request: OutputTractionMessageRequest):
        """Constructor.

        Args:
            tube_request (OutputTractionMessageRequest): The request to serialize for a single tube.
        """
        self._request = tube_request

    def payload(self) -> dict[str, Any]:
        """Generate a payload with the information required by Traction.

        Returns:
            dict[str, Any]: A dictionary containing the overall payload.
        """
        return {
            "barcode": self._request.container_barcode,
            "type": self._request.container_type,
            "request": self.request_payload(self._request),
            "sample": self.sample_payload(self._request),
        }


class OutputTractionMessage(MessageProperty):
    """Class that handles the generation and publishing of a message to Traction."""

    def __init__(self):
        """Reset initial data."""
        super().__init__(Input(self))
        self._requests: list[OutputTractionMessageRequest] = []
        self._sent = False
        self._validate_certificates = get_config().CERTIFICATES_VALIDATION_ENABLED

    @property
    def origin(self) -> str:
        """The origin identifier for this message type.
        This will be appended to any errors generated via the `trigger_error` method.

        Returns:
            str: The origin identifier.
        """
        return "OutputFeedbackMessage"

    @property
    def validators(self) -> list[Callable]:
        """A list of validators to check the message is correct.

        Returns:
            list[Callable]: The list of methods to call for complete validation of this message.
        """
        return [self.check_has_requests, self.check_requests_have_all_content, self.check_no_errors]

    def create_request(self) -> OutputTractionMessageRequest:
        """Creates a new request and returns it. It will be appended to the list of requests.

        Returns:
            OutputTractionMessageRequest: The newly created request.
        """
        self._requests.append(OutputTractionMessageRequest())
        return self._requests[-1]

    def plates_attributes(self) -> list[dict[str, Any]]:
        """Prepare a payload for all the request related to plates.

        Returns:
            list[dict[str, Any]]: A list containing the payload for all the plates.
        """
        return [PlateSerializer([request]).payload() for request in self._requests if request.container_type == "wells"]

    def tubes_attributes(self) -> list[dict[str, Any]]:
        """Prepare a payload for all the requests related to tubes.

        Returns:
            list[dict[str, Any]]: A list containing the payload for all the tubes.
        """
        return [TubeSerializer(request).payload() for request in self._requests if request.container_type == "tubes"]

    @property
    def errors(self) -> list[ErrorCode]:
        """A list of errors defined for this message."""
        return self._errors

    def check_has_requests(self) -> bool:
        """Check that this message has associated requests.
        Even if there are no requests, this will not trigger an error.

        Returns:
            bool: True if there are registered requests; otherwise False.
        """
        if self._requests:
            return True

        self.trigger_error(error_codes.ERROR_23_TRACTION_MESSAGE_HAS_NO_REQUESTS)
        return False

    def check_no_errors(self) -> bool:
        """Check that the message has no errors.

        Returns:
            bool: True if there are no errors registered; otherwise False.
        """
        return not self.errors

    def check_requests_have_all_content(self) -> bool:
        """Checks that all requests provided have valid content.
        Triggers an error if any is not.

        Returns:
            bool: True if all requests validate successfully; otherwise False.
        """
        if all([request.validate() for request in self._requests]):
            return True

        self.trigger_error(error_codes.ERROR_24_TRACTION_MESSAGE_REQUESTS_HAVE_MISSING_DATA)
        return False

    def payload(self) -> dict[str, Any]:
        """Generates the payload to send to Traction.

        Returns:
            dict[str, Any]: The payload dictionary.
        """
        return {
            "data": {
                "type": "receptions",
                "attributes": {
                    "source": OUTPUT_TRACTION_MESSAGE_SOURCE,
                    "plates_attributes": self.plates_attributes(),
                    "tubes_attributes": self.tubes_attributes(),
                },
            }
        }

    def error_code_traction_problem(self, status_code: int, error_str: str) -> None:
        """Triggers an error indicating that Traction failed.

        Args:
            status_code (int): HTTP status code when sending to Traction (422, 500, etc)
            error_str (str): Error message received from the Traction endpoint.
        """
        self.trigger_error(
            error_codes.ERROR_13_TRACTION_REQUEST_FAILED, text=f"HTTP CODE: { status_code }, MSG: {error_str}"
        )

    def send(self, url: str) -> bool:
        """Sends a Traction API request to the provided URL.
        If the send fails, an error code will be recorded.

        Args:
            url (str): The URL to submit the Traction request to.

        Returns:
            bool: True if the request was sent successfully; otherwise False.
        """
        headers = {"Content-type": "application/vnd.api+json", "Accept": "application/vnd.api+json"}

        r = post(url, headers=headers, data=dumps(self.payload()), verify=self._validate_certificates)

        self._sent = r.status_code == codes.created
        if not self._sent:
            problem = r.text
            self.error_code_traction_problem(r.status_code, problem)

        return self._sent

    @singledispatchmethod
    def add_to_message_property(self, message_property: MessageProperty) -> None:
        super().add_to_message_property(message_property)

    @add_to_message_property.register
    def _(self, feedback_message: OutputFeedbackMessage) -> None:
        """Adds error information to the an OutputFeedbackMessage.
        Also sets the operation_was_error_free to False if the message has not been sent.

        Args:
            feedback_message (OutputFeedbackMessage): The OutputFeedbackMessage to add errors to.
        """
        if not self._sent:
            feedback_message.operation_was_error_free = False
        if len(self._errors) > 0:
            for error_code in self._errors:
                feedback_message.add_error(error_code)
