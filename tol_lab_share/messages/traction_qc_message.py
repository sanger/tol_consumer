import logging
from json import dumps
from typing import Any, Callable, Dict, List, Optional

from requests import codes, post

from tol_lab_share import error_codes
from tol_lab_share.constants import OUTPUT_TRACTION_MESSAGE_SOURCE
from tol_lab_share.error_codes import ErrorCode
from tol_lab_share.helpers import get_config
from tol_lab_share.message_properties.definitions.input import Input
from tol_lab_share.message_properties.definitions.message_property import MessageProperty
from tol_lab_share.messages.interfaces import (
    OutputFeedbackMessageInterface,
    TractionQcMessageRequestInterface,
)

logger = logging.getLogger(__name__)


class TractionQcMessageRequest(TractionQcMessageRequestInterface):
    """Class that holds the information for a traction Qc message request"""

    def __init__(self):
        """Constructor to initialize the info for the request"""
        self._sanger_sample_id = None
        self._container_barcode = None
        self._sheared_femto_fragment_size = None
        self._post_spri_concentration = None
        self._post_spri_volume = None
        self._final_nano_drop_280 = None
        self._final_nano_drop_230 = None
        self._final_nano_drop = None
        self._shearing_qc_comments = None
        self._date_submitted_utc = None

    def validate(self) -> bool:
        """Checks that we have all required information and that it is valid before
        marking this request as valid."""
        return (
            (self._sanger_sample_id is not None)
            and (self._container_barcode is not None)
            and (self._sheared_femto_fragment_size is not None)
            and (self._post_spri_concentration is not None)
            and (self._post_spri_volume is not None)
            and (self._final_nano_drop_280 is not None)
            and (self._final_nano_drop_230 is not None)
            and (self._final_nano_drop is not None)
            and (self._shearing_qc_comments is not None)
            and (self._date_submitted_utc is not None)
        )

    @property
    def container_barcode(self) -> Optional[str]:
        """Gets the container barcode for this request."""
        return self._container_barcode

    @container_barcode.setter
    def container_barcode(self, value: Optional[str]) -> None:
        """Sets the container barcode for this request."""
        self._container_barcode = value

    @property
    def sanger_sample_id(self) -> Optional[str]:
        """Gets the Sanger sample id for this request."""
        return self._sanger_sample_id

    @sanger_sample_id.setter
    def sanger_sample_id(self, value: Optional[str]) -> None:
        """Sets the Sanger sample id for this request."""
        self._sanger_sample_id = value

    @property
    def sheared_femto_fragment_size(self) -> Optional[str]:
        return self._sheared_femto_fragment_size

    @sheared_femto_fragment_size.setter
    def sheared_femto_fragment_size(self, value: Optional[str]) -> None:
        self._sheared_femto_fragment_size = value

    @property
    def post_spri_concentration(self) -> Optional[str]:
        return self._post_spri_concentration

    @post_spri_concentration.setter
    def post_spri_concentration(self, value: Optional[str]) -> None:
        self._post_spri_concentration = value

    @property
    def post_spri_volume(self) -> Optional[str]:
        return self._post_spri_volume

    @post_spri_volume.setter
    def post_spri_volume(self, value: Optional[str]) -> None:
        self._post_spri_volume = value

    @property
    def final_nano_drop_280(self) -> Optional[str]:
        return self._final_nano_drop_280

    @final_nano_drop_280.setter
    def final_nano_drop_280(self, value: Optional[str]) -> None:
        self._final_nano_drop_280 = value

    @property
    def final_nano_drop_230(self) -> Optional[str]:
        return self._final_nano_drop_230

    @final_nano_drop_230.setter
    def final_nano_drop_230(self, value: Optional[str]) -> None:
        self._final_nano_drop_230 = value

    @property
    def final_nano_drop(self) -> Optional[str]:
        return self._final_nano_drop

    @final_nano_drop.setter
    def final_nano_drop(self, value: Optional[str]) -> None:
        self._final_nano_drop = value

    @property
    def shearing_qc_comments(self) -> Optional[str]:
        return self._shearing_qc_comments

    @shearing_qc_comments.setter
    def shearing_qc_comments(self, value: Optional[str]) -> None:
        self._shearing_qc_comments = value

    @property
    def date_submitted_utc(self) -> Optional[float]:
        return self._date_submitted_utc

    @date_submitted_utc.setter
    def date_submitted_utc(self, value: Optional[float]) -> None:
        self._date_submitted_utc = value

    def serializer(self):
        """Returns a serializer instance to handle the generation of the message for this request.
        Returns:
        RequestSerializer instance for this request
        """
        return QcRequestSerializer(self)


class QcRequestSerializer:
    """Class to manage the serialization to JSON of the request received as argument in the constructor."""

    def __init__(self, instance: TractionQcMessageRequest):
        """Constructor that sets initial state of the instance.
        Parameters:
        instance (TractionQcMessageRequest) request that we want to serialize
        """
        self.instance = instance

    def payload(self) -> Dict[str, Any]:
        """Constructs the payload with qc data.
        Returns:
        Dic[str,str] with all the required payload information for Traction
        """
        obj = {
            "sheared_femto_fragment_size": self.instance.sheared_femto_fragment_size,
            "post_spri_concentration": self.instance.post_spri_concentration,
            "post_spri_volume": self.instance.post_spri_volume,
            "final_nano_drop_280": self.instance.final_nano_drop_280,
            "final_nano_drop_230": self.instance.final_nano_drop_230,
            "final_nano_drop": self.instance.final_nano_drop,
            "shearing_qc_comments": self.instance.shearing_qc_comments,
            "sample_external_id": self.instance.sanger_sample_id,
            "labware_barcode": self.instance.container_barcode,
            "date_submitted": self.instance.date_submitted_utc,
        }
        return self.clear_empty_value_keys(obj)

    def clear_empty_value_keys(self, obj: Dict[str, Any]) -> Dict[str, Any]:
        return {k: v for k, v in obj.items() if v}


class TractionQcMessage(MessageProperty):
    """Class that handle the generation and publishing of a QC message to Traction"""

    def __init__(self):
        """Resets initial data"""
        super().__init__(Input(self))
        self._requests: Dict[int, TractionQcMessageRequest] = {}
        self._sent = False
        self._validate_certificates = get_config().CERTIFICATES_VALIDATION_ENABLED

    @property
    def origin(self) -> str:
        """Default origin identifier. This will be appended to any errors generated to know
        where it was originated when we received"""
        return "TractionQcMessage"

    @property
    def validators(self) -> List[Callable]:
        """List of validators to check the message is correct before sending"""
        return [self.check_has_requests, self.check_requests_have_all_content, self.check_no_errors]

    def requests(self, position: int) -> TractionQcMessageRequestInterface:
        """Returns the request at position position from this message. If there is no request there it
        will create a new instance and return it.

        Args:
            position (int) position that we want to return.

        Returns:
            TractionQcMessageRequest at the specified position.
        """
        if position not in self._requests:
            self._requests[position] = TractionQcMessageRequest()

        return self._requests[position]

    def request_attributes(self) -> List[Dict[str, Any]]:
        """Returns a list with all the qc data payload for every request
        Returns:
        List[Dict[str,Any]] with all payload for all the requests
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
            self.trigger_error(error_codes.ERROR_25_TRACTION_QC_MESSAGE_HAS_NO_REQUESTS)
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
        self.trigger_error(error_codes.ERROR_26_TRACTION_QC_MESSAGE_REQUESTS_HAVE_MISSING_DATA)
        return False

    def payload(self) -> Dict[str, Any]:
        """Returns the valid payload to send to traction"""
        return {
            "data": {
                "type": "qc_receptions",
                "attributes": {
                    "source": OUTPUT_TRACTION_MESSAGE_SOURCE,
                    "qc_results_list": self.request_attributes(),
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
            error_codes.ERROR_27_TRACTION_QC_REQUEST_FAILED, text=f"HTTP CODE: { status_code }, MSG: {error_str}"
        )

    def send(self, url: str) -> bool:
        """Sends a request to Traction. If is correct returns true, if not it will trigger an error and
        return False
        Parameters:
        url (str) url where it will send the Traction qc request
        Returns:
        bool indicating if the request was successful
        """
        headers = {"Content-type": "application/vnd.api+json", "Accept": "application/vnd.api+json"}

        r = post(url, headers=headers, data=dumps(self.payload(), default=str), verify=self._validate_certificates)

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
