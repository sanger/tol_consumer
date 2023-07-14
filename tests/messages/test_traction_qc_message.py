import logging
from datetime import datetime

import pytest
import requests_mock

from tol_lab_share.messages.traction_qc_message import TractionQcMessage

logger = logging.getLogger(__name__)


class FreezeDate(datetime):
    @classmethod
    def now(cls):
        return cls(2023, 7, 11, 12, 29, 11, 564246)


datetime = FreezeDate  # type: ignore


class TestTractionQcMessage:
    @pytest.fixture()
    def valid_traction_qc_message(self):
        traction_qc_message = TractionQcMessage()
        traction_qc_message.requests(0).supplier_sample_name = "supplier_sample_name_DDD"
        traction_qc_message.requests(0).container_barcode = "FD20706500"
        traction_qc_message.requests(0).sheared_femto_fragment_size = "5"
        traction_qc_message.requests(0).post_spri_concentration = "10"
        traction_qc_message.requests(0).post_spri_volume = "20"
        traction_qc_message.requests(0).final_nano_drop_280 = "280"
        traction_qc_message.requests(0).final_nano_drop_230 = "230"
        traction_qc_message.requests(0).final_nano_drop = "200"
        traction_qc_message.requests(0).shearing_qc_comments = "Comments"
        traction_qc_message.requests(0).date_submitted_utc = datetime.now().timestamp() * 1000
        traction_qc_message.requests(0).priority_level = "Medium"
        traction_qc_message.requests(0).date_required_by = "Long Read"
        traction_qc_message.requests(0).reason_for_priority = "Reason goes here"

        traction_qc_message.requests(1).supplier_sample_name = "supplier_sample_name_DDD2"
        traction_qc_message.requests(1).container_barcode = "FD20706501"
        traction_qc_message.requests(1).sheared_femto_fragment_size = "9"
        traction_qc_message.requests(1).post_spri_concentration = "10"
        traction_qc_message.requests(1).post_spri_volume = "30"
        traction_qc_message.requests(1).final_nano_drop_280 = "180"
        traction_qc_message.requests(1).final_nano_drop_230 = "130"
        traction_qc_message.requests(1).final_nano_drop = "100"
        traction_qc_message.requests(1).shearing_qc_comments = "Some comments"
        traction_qc_message.requests(1).date_submitted_utc = datetime.now().timestamp() * 1000
        traction_qc_message.requests(1).priority_level = "High"
        traction_qc_message.requests(1).date_required_by = "Long Read"
        traction_qc_message.requests(1).reason_for_priority = "Reason goes here"

        return traction_qc_message

    @pytest.fixture()
    def invalid_traction_qc_message(self):
        traction_qc_message = TractionQcMessage()
        traction_qc_message.requests(0).sheared_femto_fragment_size = "5"
        traction_qc_message.requests(0).priority_level = "Medium"
        traction_qc_message.requests(0).date_required_by = "Long Read"
        traction_qc_message.requests(0).reason_for_priority = "Reason goes here"

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
                    "qc_results_list": [
                        {
                            "final_nano_drop": "200",
                            "final_nano_drop_230": "230",
                            "final_nano_drop_280": "280",
                            "post_spri_concentration": "10",
                            "post_spri_volume": "20",
                            "sheared_femto_fragment_size": "5",
                            "shearing_qc_comments": "Comments",
                            "date_required_by": "Long Read",
                            "date_submitted": datetime.now().timestamp() * 1000,
                            "labware_barcode": "FD20706500",
                            "priority_level": "Medium",
                            "reason_for_priority": "Reason goes here",
                            "sample_external_id": "supplier_sample_name_DDD",
                        },
                        {
                            "final_nano_drop": "100",
                            "final_nano_drop_230": "130",
                            "final_nano_drop_280": "180",
                            "post_spri_concentration": "10",
                            "post_spri_volume": "30",
                            "sheared_femto_fragment_size": "9",
                            "shearing_qc_comments": "Some comments",
                            "date_required_by": "Long Read",
                            "date_submitted": datetime.now().timestamp() * 1000,
                            "labware_barcode": "FD20706501",
                            "priority_level": "High",
                            "reason_for_priority": "Reason goes here",
                            "sample_external_id": "supplier_sample_name_DDD2",
                        },
                    ],
                    "source": "tol-lab-share.tol",
                },
                "type": "qc_receptions",
            }
        }

        assert payload == expected_payload

    def test_can_add_to_feedback_message_on_success(
        self, config, valid_traction_qc_message, valid_feedback_message, traction_qc_success_response
    ):
        feedback = valid_feedback_message
        with requests_mock.Mocker() as m:
            m.post(config.TRACTION_QC_URL, json=traction_qc_success_response, status_code=201)
            valid_traction_qc_message.send(config.TRACTION_QC_URL)
        valid_traction_qc_message.add_to_feedback_message(feedback)
        assert len(feedback.errors) == 0
        assert feedback.operation_was_error_free

    def test_can_add_to_feedback_message_when_errors(self, invalid_traction_qc_message, valid_feedback_message):
        assert not invalid_traction_qc_message.validate()
        feedback = valid_feedback_message
        invalid_traction_qc_message.add_to_feedback_message(feedback)
        assert len(feedback.errors) > 0
        assert not feedback.operation_was_error_free
