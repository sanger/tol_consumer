from unittest.mock import MagicMock, patch

import pytest
import requests_mock

from tol_lab_share.constants import RABBITMQ_SUBJECT_CREATE_LABWARE_FEEDBACK
from tol_lab_share.messages.rabbit.consumed import CreateLabwareMessage
from tol_lab_share.messages.rabbit.published import CreateLabwareFeedbackMessage
from tol_lab_share.processors.create_labware_processor import CreateLabwareProcessor


class TestCreateLabwareProcessor:
    def test_can_be_initialised(self, config):
        schema_registry = MagicMock()
        assert CreateLabwareProcessor(schema_registry, MagicMock(), config) is not None

    def test_valid_input_can_run_process(
        self,
        config,
        valid_create_labware_message,
        traction_success_creation_response,
        traction_qc_success_response,
        taxonomy_record,
    ):
        with patch(
            "tol_lab_share.messages.rabbit.published.create_labware_feedback_message.AvroEncoderBinary"
        ) as mock_avro_encoder:
            mocked_instance_encoder = MagicMock()
            mock_avro_encoder.return_value = mocked_instance_encoder

            schema_registry = MagicMock()
            publisher = MagicMock()

            instance = CreateLabwareProcessor(schema_registry, publisher, config)

            with requests_mock.Mocker() as m:
                m.get(config.EBI_TAXONOMY_URL + "/10090", json=taxonomy_record)
                m.post(config.TRACTION_URL, json=traction_success_creation_response, status_code=201)
                m.post(config.TRACTION_QC_URL, json=traction_qc_success_response, status_code=201)
                assert instance.process(valid_create_labware_message) is True
                input = CreateLabwareMessage(valid_create_labware_message)
                output_feedback_message = CreateLabwareFeedbackMessage()
                assert instance.send_qc_data_to_traction(input, output_feedback_message) is True

            mock_avro_encoder.assert_called_once_with(schema_registry, RABBITMQ_SUBJECT_CREATE_LABWARE_FEEDBACK)
            mocked_instance_encoder.encode.assert_called_once_with(
                [
                    {
                        "sourceMessageUuid": "b01aa0ad-7b19-4f94-87e9-70d74fb8783c",
                        "countOfTotalSamples": 2,
                        "countOfValidSamples": 2,
                        "operationWasErrorFree": True,
                        "errors": [],
                    }
                ]
            )

            publisher.publish_message.assert_called_once()

    @pytest.mark.parametrize(
        "error_code_checks",
        ["tol_lab_share.processors.create_labware_processor.error_codes.ERROR_17_INPUT_MESSAGE_INVALID"],
    )
    def test_invalid_input_triggers_error(
        self,
        config,
        invalid_create_labware_message,
        traction_success_creation_response,
        traction_qc_success_response,
        taxonomy_record,
        error_code_checks,
    ):
        with patch(error_code_checks) as error_code:
            with patch(
                "tol_lab_share.messages.rabbit.published.create_labware_feedback_message.AvroEncoderBinary"
            ) as mock_avro_encoder:
                mocked_instance_encoder = MagicMock()
                mock_avro_encoder.return_value = mocked_instance_encoder
                schema_registry = MagicMock()
                publisher = MagicMock()

                instance = CreateLabwareProcessor(schema_registry, publisher, config)

                with requests_mock.Mocker() as m:
                    m.get(config.EBI_TAXONOMY_URL + "/10090", json=taxonomy_record)
                    m.post(config.TRACTION_URL, json=traction_success_creation_response)
                    m.post(config.TRACTION_QC_URL, json=traction_qc_success_response, status_code=201)
                    assert instance.process(invalid_create_labware_message) is True
                    error_code.trigger.assert_called()

                mock_avro_encoder.assert_called_once_with(schema_registry, RABBITMQ_SUBJECT_CREATE_LABWARE_FEEDBACK)
                mocked_instance_encoder.encode.assert_called_once_with(
                    [
                        {
                            "sourceMessageUuid": "b01aa0ad7b19-4f94-87e9-70d74fb8783c",
                            "countOfTotalSamples": 2,
                            "countOfValidSamples": 0,
                            "operationWasErrorFree": False,
                            "errors": [
                                {
                                    "typeId": 2,
                                    "field": "message_uuid",
                                    "origin": "plate",
                                    "description": (
                                        'Uuid has wrong format, instance: "MessageUuid",'
                                        " text: \"input: b'b01aa0ad7b19-4f94-87e9-70d74fb8783c'\""
                                    ),
                                },
                                {
                                    "typeId": 2,
                                    "field": "final_nano_drop",
                                    "origin": "sample",
                                    "description": 'Not string, instance: "StringValue"',
                                },
                                {
                                    "typeId": 7,
                                    "field": "location",
                                    "origin": "sample",
                                    "description": 'Not valid location, instance: "Location", text: "input: A001"',
                                },
                                {
                                    "typeId": 7,
                                    "field": "location",
                                    "origin": "sample",
                                    "description": 'Not valid location, instance: "Location", text: "input: B001"',
                                },
                                {
                                    "typeId": 2,
                                    "field": "post_spri_volume",
                                    "origin": "sample",
                                    "description": 'Not string, instance: "StringValue"',
                                },
                            ],
                        }
                    ]
                )
                publisher.publish_message.assert_called_once()

    @pytest.mark.parametrize(
        "error_code_checks",
        ["tol_lab_share.processors.create_labware_processor.error_codes.ERROR_16_PROBLEM_TALKING_WITH_TRACTION"],
    )
    def test_reports_error_when_traction_responds_with_422(
        self, config, valid_create_labware_message, taxonomy_record, error_code_checks
    ):
        with patch(error_code_checks) as error_code:
            with patch(
                "tol_lab_share.messages.rabbit.published.create_labware_feedback_message.AvroEncoderBinary"
            ) as mock_avro_encoder:
                mocked_instance_encoder = MagicMock()
                mock_avro_encoder.return_value = mocked_instance_encoder

                schema_registry = MagicMock()
                publisher = MagicMock()

                instance = CreateLabwareProcessor(schema_registry, publisher, config)

                with requests_mock.Mocker() as m:
                    m.get(config.EBI_TAXONOMY_URL + "/10090", json=taxonomy_record)
                    m.post(config.TRACTION_URL, text="This is an error", status_code=422)

                    assert instance.process(valid_create_labware_message) is True
                    error_code.trigger.assert_called()

                mock_avro_encoder.assert_called_once_with(schema_registry, RABBITMQ_SUBJECT_CREATE_LABWARE_FEEDBACK)
                mocked_instance_encoder.encode.assert_called_once_with(
                    [
                        {
                            "sourceMessageUuid": "b01aa0ad-7b19-4f94-87e9-70d74fb8783c",
                            "countOfTotalSamples": 2,
                            "countOfValidSamples": 2,
                            "operationWasErrorFree": False,
                            "errors": [
                                {
                                    "typeId": 13,
                                    "field": "dict",
                                    "origin": "root",
                                    "description": (
                                        'Traction send request failed, instance: "TractionReceptionMessage",'
                                        ' text: "HTTP CODE: 422, MSG: This is an error"'
                                    ),
                                }
                            ],
                        }
                    ]
                )
                publisher.publish_message.assert_called_once()

    def test_reports_error_when_traction_responds_with_500(self, config, valid_create_labware_message, taxonomy_record):
        with patch(
            "tol_lab_share.messages.rabbit.published.create_labware_feedback_message.AvroEncoderBinary"
        ) as mock_avro_encoder:
            mocked_instance_encoder = MagicMock()
            mock_avro_encoder.return_value = mocked_instance_encoder

            schema_registry = MagicMock()
            publisher = MagicMock()

            instance = CreateLabwareProcessor(schema_registry, publisher, config)

            with requests_mock.Mocker() as m:
                m.get(config.EBI_TAXONOMY_URL + "/10090", json=taxonomy_record)
                m.post(config.TRACTION_URL, text="Another error", status_code=500)
                assert instance.process(valid_create_labware_message) is True

            mock_avro_encoder.assert_called_once_with(schema_registry, RABBITMQ_SUBJECT_CREATE_LABWARE_FEEDBACK)
            mocked_instance_encoder.encode.assert_called_once_with(
                [
                    {
                        "sourceMessageUuid": "b01aa0ad-7b19-4f94-87e9-70d74fb8783c",
                        "countOfTotalSamples": 2,
                        "countOfValidSamples": 2,
                        "operationWasErrorFree": False,
                        "errors": [
                            {
                                "typeId": 13,
                                "field": "dict",
                                "origin": "root",
                                "description": (
                                    'Traction send request failed, instance: "TractionReceptionMessage",'
                                    ' text: "HTTP CODE: 500, MSG: Another error"'
                                ),
                            }
                        ],
                    }
                ]
            )
            publisher.publish_message.assert_called_once()

    @pytest.mark.parametrize(
        "error_code_checks",
        ["tol_lab_share.processors.create_labware_processor.error_codes.ERROR_18_FEEDBACK_MESSAGE_INVALID"],
    )
    def test_calls_trigger_on_error_code_when_feedback_message_is_invalid(
        self,
        config,
        valid_create_labware_message,
        taxonomy_record,
        error_code_checks,
        traction_success_creation_response,
        traction_qc_success_response,
    ):
        # Mock feedback message to not validate
        feedback_message = MagicMock()
        feedback_message.validate.return_value = False

        with patch(error_code_checks) as error_code:
            with patch(
                "tol_lab_share.processors.create_labware_processor.CreateLabwareFeedbackMessage",
                return_value=feedback_message,
            ):
                with patch("tol_lab_share.messages.rabbit.published.create_labware_feedback_message.AvroEncoderBinary"):
                    schema_registry = MagicMock()
                    publisher = MagicMock()

                    instance = CreateLabwareProcessor(schema_registry, publisher, config)

                    with requests_mock.Mocker() as m:
                        m.get(config.EBI_TAXONOMY_URL + "/10090", json=taxonomy_record)
                        m.post(config.TRACTION_URL, json=traction_success_creation_response, status_code=201)
                        m.post(config.TRACTION_QC_URL, json=traction_qc_success_response, status_code=201)

                        instance.process(valid_create_labware_message)
                        error_code.trigger.assert_called()

    @pytest.mark.parametrize(
        "error_code_checks",
        ["tol_lab_share.processors.create_labware_processor.error_codes.ERROR_28_PROBLEM_TALKING_TO_TRACTION"],
    )
    def test_calls_trigger_on_error_code_when_traction_qc_responds_with_422(
        self,
        config,
        valid_create_labware_message,
        taxonomy_record,
        error_code_checks,
        traction_success_creation_response,
    ):
        with patch(error_code_checks) as error_code:
            with patch(
                "tol_lab_share.messages.rabbit.published.create_labware_feedback_message.AvroEncoderBinary"
            ) as mock_avro_encoder:
                mocked_instance_encoder = MagicMock()
                mock_avro_encoder.return_value = mocked_instance_encoder

                schema_registry = MagicMock()
                publisher = MagicMock()

                instance = CreateLabwareProcessor(schema_registry, publisher, config)

                with requests_mock.Mocker() as m:
                    m.get(config.EBI_TAXONOMY_URL + "/10090", json=taxonomy_record)
                    m.post(config.TRACTION_URL, json=traction_success_creation_response, status_code=201)
                    m.post(config.TRACTION_QC_URL, text="This is an error", status_code=422)
                    input = CreateLabwareMessage(valid_create_labware_message)
                    output_feedback_message = CreateLabwareFeedbackMessage()

                    process_result = instance.process(valid_create_labware_message)
                    assert process_result is True

                    send_qc_result = instance.send_qc_data_to_traction(input, output_feedback_message)
                    assert send_qc_result is False

                    error_code.trigger.assert_called()

                mock_avro_encoder.assert_called_once_with(schema_registry, RABBITMQ_SUBJECT_CREATE_LABWARE_FEEDBACK)
                mocked_instance_encoder.encode.assert_called_once_with(
                    [
                        {
                            "sourceMessageUuid": "b01aa0ad-7b19-4f94-87e9-70d74fb8783c",
                            "countOfTotalSamples": 2,
                            "countOfValidSamples": 2,
                            "operationWasErrorFree": False,
                            "errors": [
                                {
                                    "typeId": 27,
                                    "field": "dict",
                                    "origin": "root",
                                    "description": (
                                        'Traction qc send request failed, instance: "TractionQcMessage",'
                                        ' text: "HTTP CODE: 422, MSG: This is an error"'
                                    ),
                                }
                            ],
                        }
                    ]
                )
                publisher.publish_message.assert_called_once()

    @pytest.mark.parametrize(
        "error_code_checks",
        ["tol_lab_share.processors.create_labware_processor.error_codes.ERROR_28_PROBLEM_TALKING_TO_TRACTION"],
    )
    def test_calls_trigger_on_error_code_when_traction_qc_responds_with_500(
        self,
        config,
        valid_create_labware_message,
        traction_success_creation_response,
        taxonomy_record,
        error_code_checks,
    ):
        with patch(error_code_checks) as error_code:
            with patch(
                "tol_lab_share.messages.rabbit.published.create_labware_feedback_message.AvroEncoderBinary"
            ) as mock_avro_encoder:
                mocked_instance_encoder = MagicMock()
                mock_avro_encoder.return_value = mocked_instance_encoder

                schema_registry = MagicMock()
                publisher = MagicMock()

                instance = CreateLabwareProcessor(schema_registry, publisher, config)

                with requests_mock.Mocker() as m:
                    m.get(config.EBI_TAXONOMY_URL + "/10090", json=taxonomy_record)
                    m.post(config.TRACTION_URL, json=traction_success_creation_response, status_code=201)
                    m.post(config.TRACTION_QC_URL, text="This is an internal server error", status_code=500)
                    input = CreateLabwareMessage(valid_create_labware_message)
                    output_feedback_message = CreateLabwareFeedbackMessage()

                    process_result = instance.process(valid_create_labware_message)
                    assert process_result is True

                    send_qc_result = instance.send_qc_data_to_traction(input, output_feedback_message)
                    assert send_qc_result is False

                    error_code.trigger.assert_called()

                mock_avro_encoder.assert_called_once_with(schema_registry, RABBITMQ_SUBJECT_CREATE_LABWARE_FEEDBACK)
                mocked_instance_encoder.encode.assert_called_once_with(
                    [
                        {
                            "sourceMessageUuid": "b01aa0ad-7b19-4f94-87e9-70d74fb8783c",
                            "countOfTotalSamples": 2,
                            "countOfValidSamples": 2,
                            "operationWasErrorFree": False,
                            "errors": [
                                {
                                    "typeId": 27,
                                    "field": "dict",
                                    "origin": "root",
                                    "description": (
                                        'Traction qc send request failed, instance: "TractionQcMessage",'
                                        ' text: "HTTP CODE: 500, MSG: This is an internal server error"'
                                    ),
                                }
                            ],
                        }
                    ]
                )
                publisher.publish_message.assert_called_once()
