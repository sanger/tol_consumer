from tol_lab_share.messages.traction_qc_message import TractionQcMessage
from tol_lab_share.messages.output_feedback_message import OutputFeedbackMessage

import sys
import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime
import logging
logger = logging.getLogger(__name__)


class FreezeDate(datetime):
    @classmethod
    def now(cls):
        return cls(2023, 7, 11, 12, 29, 11, 564246)
datetime = FreezeDate

class TestTractionQcMessage:
    @pytest.fixture()
    def valid_traction_qc_message(self):
        traction_qc_message = TractionQcMessage()
        sample_pos = 0
        traction_qc_message.requests(sample_pos).sample_uuid = "8860a6b4-82e2-451c-aba2-a3129c38c0fc"
        traction_qc_message.requests(sample_pos).container_barcode = "1234"
        traction_qc_message.requests(sample_pos).sheared_femto_fragment_size = "5"
        traction_qc_message.requests(sample_pos).post_spri_concentration = "10"
        traction_qc_message.requests(sample_pos).post_spri_volume = "20"
        traction_qc_message.requests(sample_pos).final_nano_drop_280 = "280"
        traction_qc_message.requests(sample_pos).final_nano_drop_230 = "230"
        traction_qc_message.requests(sample_pos).final_nano_drop = "200"
        traction_qc_message.requests(sample_pos).shearing_qc_comments = "Comments" 
        traction_qc_message.requests(sample_pos).date_submitted_utc = datetime.now().timestamp() * 1000
        traction_qc_message.requests(sample_pos).priority_level = "Medium"
        traction_qc_message.requests(sample_pos).date_required_by = "Long Read"
        traction_qc_message.requests(sample_pos).reason_for_priority = "Reason goes here"
        
        return traction_qc_message

    @pytest.fixture()
    def invalid_traction_qc_message(self):
        traction_qc_message = TractionQcMessage()
        sample_pos = 0
        traction_qc_message.requests(sample_pos).sheared_femto_fragment_size = "5"
        traction_qc_message.requests(sample_pos).priority_level = "Medium"
        traction_qc_message.requests(sample_pos).date_required_by = "Long Read"
        traction_qc_message.requests(sample_pos).reason_for_priority = "Reason goes here"
        
        return traction_qc_message

    def test_can_initialize_traction_qc_message(self):
        assert TractionQcMessage() is not None
    
    def test_validate_traction_qc_message(self, valid_traction_qc_message, invalid_traction_qc_message):
        traction_qc_message = TractionQcMessage()
        assert not traction_qc_message.validate()
        assert not invalid_traction_qc_message.validate()
        assert valid_traction_qc_message.validate()

    def test_can_generate_correct_payload(self, valid_traction_qc_message):
        payload = valid_traction_qc_message.payload()
        
        expected_payload = {
            "data": {
                "attributes": {
                    "request_attributes": [
                        {
                        "qc_data": {
                            "final_nano_drop": "200",
                            "final_nano_drop_230": "230",
                            "final_nano_drop_280": "280",
                            "post_spri_concentration": "10",
                            "post_spri_volume": "20",
                            "sheared_femto_fragment_size": "5",
                            "shearing_qc_comments": "Comments"
                        },
                        "sample": {
                            "date_required_by": "Long Read",
                            "date_submitted": datetime.now().timestamp() * 1000,
                            "labware_barcode": "1234",
                            "priority_level": "Medium",
                            "reason_for_priority": "Reason goes here",
                            "sample_external_id": "8860a6b4-82e2-451c-aba2-a3129c38c0fc"
                        }
                        }
                    ],
                    "source": "tol-lab-share.tol"
                },
                "type": "qc_results"
            }
        }

        assert payload == expected_payload
