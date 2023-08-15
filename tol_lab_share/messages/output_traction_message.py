from typing import Dict, Optional, List, Callable, Any
from json import dumps
from datetime import datetime
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
    OUTPUT_TRACTION_MESSAGE_SOURCE,
)
from tol_lab_share import error_codes
from tol_lab_share.error_codes import ErrorCode
from tol_lab_share.helpers import get_config


class OutputTractionMessageRequest(OutputTractionMessageRequestInterface):
    """Class that manages the information of a single Traction request instance
    as part of the Traction message
    """

    def __init__(self):
        """Constructor that initializes all info for a single request"""
        self._library_type = None
        self._study_uuid = None
        self._sample_name = None
        self._sample_uuid = None
        self._container_barcode = None
        self._container_location = None
        self._container_type = None
        self._species = None
        self._cost_code = None
        self._priority_level = None
        self._sanger_sample_id = None
        self._supplier_name = None
        self._taxon_id = None
        self._donor_id = None
        self._country_of_origin = None
        self._accession_number = None
        self._date_of_sample_collection = None

    def validate(self) -> bool:
        """Checks that we have all required information and that it is valid before
        marking this request as valid."""
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
    def sanger_sample_id(self) -> Optional[str]:
        """Gets the sanger_sample_id value for this request"""
        return self._sanger_sample_id

    @sanger_sample_id.setter
    def sanger_sample_id(self, value: Optional[str]) -> None:
        """Sets the sanger_sample_id value for this request"""
        self._sanger_sample_id = value

    @property
    def date_of_sample_collection(self) -> Optional[datetime]:
        """Gets the date_of_sample_collection value for this request"""
        return self._date_of_sample_collection

    @date_of_sample_collection.setter
    def date_of_sample_collection(self, value: Optional[datetime]) -> None:
        """Sets the date_of_sample_collection value for this request"""
        self._date_of_sample_collection = value

    @property
    def supplier_name(self) -> Optional[str]:
        """Gets the supplier_name value for this request"""
        return self._supplier_name

    @supplier_name.setter
    def supplier_name(self, value: Optional[str]) -> None:
        """Sets the supplier_name value for this request"""
        self._supplier_name = value

    @property
    def taxon_id(self) -> Optional[str]:
        """Gets the taxon_id value for this request"""
        return self._taxon_id

    @taxon_id.setter
    def taxon_id(self, value: Optional[str]) -> None:
        """Sets the taxon_id value for this request"""
        self._taxon_id = value

    @property
    def donor_id(self) -> Optional[str]:
        """Gets the donor_id value for this request"""
        return self._donor_id

    @donor_id.setter
    def donor_id(self, value: Optional[str]) -> None:
        """Sets the donor_id value for this request"""
        self._donor_id = value

    @property
    def country_of_origin(self) -> Optional[str]:
        """Gets the country_of_origin value for this request"""
        return self._country_of_origin

    @country_of_origin.setter
    def country_of_origin(self, value: Optional[str]) -> None:
        """Sets the country_of_origin value for this request"""
        self._country_of_origin = value

    @property
    def accession_number(self) -> Optional[str]:
        """Gets the accession_number value for this request"""
        return self._accession_number

    @accession_number.setter
    def accession_number(self, value: Optional[str]) -> None:
        """Sets the accession_number value for this request"""
        self._accession_number = value

    @property
    def species(self) -> Optional[str]:
        """Gets the species value for this request"""
        return self._species

    @species.setter
    def species(self, value: Optional[str]) -> None:
        """Sets the species value for this request"""
        self._species = value

    @property
    def cost_code(self) -> Optional[str]:
        """Gets the cost_code value for this request"""
        return self._cost_code

    @cost_code.setter
    def cost_code(self, value: Optional[str]) -> None:
        """Sets the cost_code value for this request"""
        self._cost_code = value

    @property
    def container_type(self) -> Optional[str]:
        """Gets the container type value for this request. ('wells' or 'tubes')"""
        return self._container_type

    @container_type.setter
    def container_type(self, value: Optional[str]) -> None:
        """Sets the container type value for this request. ('wells' or 'tubes')"""
        self._container_type = value

    @property
    def container_location(self) -> Optional[str]:
        """Gets the container location for this request. Eg: 'A01'"""
        return self._container_location

    @container_location.setter
    def container_location(self, value: Optional[str]) -> None:
        """Sets the container location for this request. Eg: 'A01'"""
        self._container_location = value

    @property
    def container_barcode(self) -> Optional[str]:
        """Gets the container barcode for this request."""
        return self._container_barcode

    @container_barcode.setter
    def container_barcode(self, value: Optional[str]) -> None:
        """Sets the container barcode for this request."""
        self._container_barcode = value

    @property
    def sample_uuid(self) -> Optional[str]:
        """Gets the sample uuid for this request."""
        return self._sample_uuid

    @sample_uuid.setter
    def sample_uuid(self, value: Optional[str]) -> None:
        """Sets the sample uuid for this request."""
        self._sample_uuid = value

    @property
    def sample_name(self) -> Optional[str]:
        """Gets the sample name for this request."""
        return self._sample_name

    @sample_name.setter
    def sample_name(self, value: Optional[str]) -> None:
        """Sets the sample name for this request."""
        self._sample_name = value

    @property
    def library_type(self) -> Optional[str]:
        """Gets the library type for this request."""
        return self._library_type

    @library_type.setter
    def library_type(self, value: Optional[str]) -> None:
        """Sets the library type for this request."""
        self._library_type = value

    @property
    def study_uuid(self) -> Optional[str]:
        """Gets the study uuid for this request."""
        return self._study_uuid

    @study_uuid.setter
    def study_uuid(self, value: Optional[str]) -> None:
        """Sets the study uuid for this request."""
        self._study_uuid = value

    @property
    def priority_level(self) -> Optional[str]:
        return self._priority_level

    @priority_level.setter
    def priority_level(self, value: Optional[str]) -> None:
        self._priority_level = value

    def serializer(self):
        """Returns a serializer instance to handle the generation of the message for this request.
        Returns:
        RequestSerializer instance for this request
        """
        return RequestSerializer(self)


class RequestSerializer:
    """Class to manage the serialization to JSON of the request received as argument in the constructor."""

    def __init__(self, instance: OutputTractionMessageRequest):
        """Constructor that sets initiali state of the instance.
        Parameters:
        instance (OutputTractionMessageRequest) request that we want to serialize
        """
        self.instance = instance

    def is_ont_library_type(self) -> bool:
        """Flag boolean method that identifies if the library type is ONT.
        Returns:
        boolean indicating if the library type is ONT or not
        """
        return bool(self.instance.library_type and ("ONT" in self.instance.library_type))

    def request_payload(self) -> Dict[str, Any]:
        """Generates the correct payload depending on the library type for the current request.
        Returns:
        Dic[str,str] with the required information to send for this request to Traction
        """
        if self.is_ont_library_type():
            return {
                "data_type": "basecalls",
                "library_type": self.instance.library_type,
                "external_study_id": self.instance.study_uuid,
                "cost_code": self.instance.cost_code,
            }
        else:
            return {
                "library_type": self.instance.library_type,
                "external_study_id": self.instance.study_uuid,
                "cost_code": self.instance.cost_code,
            }

    def sample_payload(self) -> Dict[str, Any]:
        """Generates the correct payload for the sample defined in this request
        Returns:
        Dic[str,str] with the required sample information to send for this request to Traction
        """
        collection_date = None
        if self.instance.date_of_sample_collection is not None:
            collection_date = self.instance.date_of_sample_collection.strftime("%Y-%m-%d")
        return {
            "name": self.instance.sample_name,
            "external_id": self.instance.sample_uuid,
            "species": self.instance.species,
            "priority_level": self.instance.priority_level,
            "sanger_sample_id": self.instance.sanger_sample_id,
            "supplier_name": self.instance.supplier_name,
            "taxon_id": self.instance.taxon_id,
            "donor_id": self.instance.donor_id,
            "country_of_origin": self.instance.country_of_origin,
            "accession_number": self.instance.accession_number,
            "date_of_sample_collection": collection_date,
        }

    def container_payload(self) -> Dict[str, Any]:
        """Generates the correct payload for the container defined in this request depending on
        the container type (tubes or wells)
        Returns:
        Dic[str,str] with the required container information to send for this request to Traction
        """
        if self.instance.container_type == "tubes":
            return {"type": self.instance.container_type, "barcode": self.instance.container_barcode}
        else:
            return {
                "type": self.instance.container_type,
                "barcode": self.instance.container_barcode,
                "position": self.instance.container_location,
            }

    def payload(self) -> Dict[str, Any]:
        """Main builder of the payload required to describe all information required for Traction:
        sample, request and container.
        Returns:
        Dic[str,str] with all the required payload information for Traction
        """
        return {
            "request": self.request_payload(),
            "sample": self.sample_payload(),
            "container": self.container_payload(),
        }


class OutputTractionMessage(MessageProperty, OutputTractionMessageInterface):
    """Class that handle the generation and publishing of a message to Traction"""

    def __init__(self):
        """Resets initial data"""
        super().__init__(Input(self))
        self._requests: Dict[int, OutputTractionMessageRequest] = {}
        self._sent = False
        self._validate_certificates = get_config().CERTIFICATES_VALIDATION_ENABLED

    @property
    def origin(self) -> str:
        """Default origin identifier. This will be appended to any errors generated to know
        where it was originated when we received"""
        return "OutputFeedbackMessage"

    @property
    def validators(self) -> List[Callable]:
        """List of validators to check the message is correct before sending"""
        return [self.check_has_requests, self.check_requests_have_all_content, self.check_no_errors]

    def requests(self, position: int) -> OutputTractionMessageRequestInterface:
        """Returns the request at position position from this message. If there is no requesrt there it
        will create a new instance and return it.
        Parameters:
        position (int) position that we want to return
        Returns:
        OutputTractionMessageRequest with the request required
        """
        if position not in self._requests:
            self._requests[position] = OutputTractionMessageRequest()

        return self._requests[position]

    def request_attributes(self) -> List[Dict[str, Any]]:
        """Returns a list with all the payloads for every request
        Returns:
        List[Dict[str,Any]] with all payloads for all the requests
        """
        return [self._requests[position].serializer().payload() for position in range(len(self._requests))]

    @property
    def errors(self) -> List[ErrorCode]:
        """List of errors defined for this message"""
        return self._errors

    def check_has_requests(self) -> bool:
        """Returns a bool identifying if the message has requests. If not it will trigger an error and
        return false.
        Returns
        bool saying if the message has requests
        """
        if len(self._requests) > 0:
            return True
        else:
            self.trigger_error(error_codes.ERROR_23_TRACTION_MESSAGE_HAS_NO_REQUESTS)
            return False

    def check_no_errors(self) -> bool:
        """Checks that a message has no errors
        Returns:
        bool indicating if there is no errors
        """
        return len(self.errors) == 0

    def check_requests_have_all_content(self) -> bool:
        """Checks that all requests provided are valid. Triggers an error if any is not.
        Returns:
        bool indicating that all requests have valid content inside.
        """
        if all([self.requests(key).validate() for key in self._requests]):
            return True
        self.trigger_error(error_codes.ERROR_24_TRACTION_MESSAGE_REQUESTS_HAVE_MISSING_DATA)
        return False

    def payload(self) -> Dict[str, Any]:
        """Returns the valid payload to send to traction"""
        return {
            "data": {
                "type": "receptions",
                "attributes": {
                    "source": OUTPUT_TRACTION_MESSAGE_SOURCE,
                    "request_attributes": self.request_attributes(),
                },
            }
        }

    def error_code_traction_problem(self, status_code: int, error_str: str) -> None:
        """Triggers an error indicating that traction failed.
        Parameters:
        status_code (int) HTTP status code when sending to traction (422, 500, etc)
        error_str (str) contents received by Traction endpoint on the request
        """
        self.trigger_error(
            error_codes.ERROR_13_TRACTION_REQUEST_FAILED, text=f"HTTP CODE: { status_code }, MSG: {error_str}"
        )

    def send(self, url: str) -> bool:
        """Sends a request to Traction. If is correct returns true, if not it will trigger an error and
        return False
        Parameters:
        url (str) url where it will send the Traction request
        Returns:
        bool indicating if the request was successful
        """
        headers = {"Content-type": "application/vnd.api+json", "Accept": "application/vnd.api+json"}

        r = post(url, headers=headers, data=dumps(self.payload()), verify=self._validate_certificates)

        self._sent = r.status_code == codes.created
        if not self._sent:
            problem = r.text
            self.error_code_traction_problem(r.status_code, problem)

        return self._sent

    def add_to_feedback_message(self, feedback_message: OutputFeedbackMessageInterface) -> None:
        """Adds the relevant information about this Traction sent to the feedback message, indicating
        if there has been any errors"""
        if not self._sent:
            feedback_message.operation_was_error_free = False
        if len(self._errors) > 0:
            for error_code in self._errors:
                feedback_message.add_error(error_code)
