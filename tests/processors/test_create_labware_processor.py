from unittest.mock import MagicMock, patch
from tol_lab_share.processors.create_labware_processor import CreateLabwareProcessor
from tol_lab_share.constants import RABBITMQ_SUBJECT_CREATE_LABWARE_FEEDBACK
import requests_mock
import pytest


def test_create_labware_processor(config):
    schema_registry = MagicMock()
    assert CreateLabwareProcessor(schema_registry, MagicMock(), config) is not None


def test_create_labware_processor_with_valid_input_can_run_process(
    config, valid_create_labware_message, traction_success_creation_response, taxonomy_record
):
    with patch("tol_lab_share.messages.output_feedback_message.AvroEncoderJson") as mock_avro_encoder:
        mocked_instance_encoder = MagicMock()
        mock_avro_encoder.return_value = mocked_instance_encoder

        schema_registry = MagicMock()
        publisher = MagicMock()

        instance = CreateLabwareProcessor(schema_registry, publisher, config)

        with requests_mock.Mocker() as m:
            m.get(config.EBI_TAXONOMY_URL + "/10090", json=taxonomy_record)
            m.post(config.TRACTION_URL, json=traction_success_creation_response, status_code=201)
            assert instance.process(valid_create_labware_message) is True

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
def test_create_labware_processor_with_invalid_input_triggers_error(
    config, invalid_create_labware_message, traction_success_creation_response, taxonomy_record, error_code_checks
):
    with patch(error_code_checks) as error_code:
        with patch("tol_lab_share.messages.output_feedback_message.AvroEncoderJson") as mock_avro_encoder:
            mocked_instance_encoder = MagicMock()
            mock_avro_encoder.return_value = mocked_instance_encoder
            schema_registry = MagicMock()
            publisher = MagicMock()

            instance = CreateLabwareProcessor(schema_registry, publisher, config)

            with requests_mock.Mocker() as m:
                m.get(config.EBI_TAXONOMY_URL + "/10090", json=taxonomy_record)
                m.post(config.TRACTION_URL, json=traction_success_creation_response)
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
                                "type_id": 2,
                                "field": "message_uuid",
                                "origin": "plate",
                                "description": (
                                    'Uuid has wrong format, instance: "MessageUuid",'
                                    " text: \"input: b'b01aa0ad7b19-4f94-87e9-70d74fb8783c'\""
                                ),
                            },
                            {
                                "type_id": 20,
                                "field": "concentration",
                                "origin": "samples[0]",
                                "description": 'The input provided is not a valid float., instance: "Concentration"',
                            },
                            {
                                "type_id": 20,
                                "field": "volume",
                                "origin": "samples[0]",
                                "description": 'The input provided is not a valid float., instance: "Volume"',
                            },
                            {
                                "type_id": 7,
                                "field": "location",
                                "origin": "samples[0]",
                                "description": 'Not valid location, instance: "Location", text: "input: A001"',
                            },
                            {
                                "type_id": 9,
                                "field": "scientific_name",
                                "origin": "samples[0]",
                                "description": 'Not valid input, instance: "ScientificNameFromTaxonId"',
                            },
                            {
                                "type_id": 20,
                                "field": "concentration",
                                "origin": "samples[1]",
                                "description": 'The input provided is not a valid float., instance: "Concentration"',
                            },
                            {
                                "type_id": 20,
                                "field": "volume",
                                "origin": "samples[1]",
                                "description": 'The input provided is not a valid float., instance: "Volume"',
                            },
                            {
                                "type_id": 7,
                                "field": "location",
                                "origin": "samples[1]",
                                "description": 'Not valid location, instance: "Location", text: "input: B001"',
                            },
                            {
                                "type_id": 9,
                                "field": "scientific_name",
                                "origin": "samples[1]",
                                "description": 'Not valid input, instance: "ScientificNameFromTaxonId"',
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
def test_create_labware_processor_when_traction_sends_422(
    config, valid_create_labware_message, taxonomy_record, error_code_checks
):
    with patch(error_code_checks) as error_code:
        with patch("tol_lab_share.messages.output_feedback_message.AvroEncoderJson") as mock_avro_encoder:
            schema_registry = MagicMock()
            publisher = MagicMock()

            instance = CreateLabwareProcessor(schema_registry, publisher, config)

            with requests_mock.Mocker() as m:
                m.get(config.EBI_TAXONOMY_URL + "/10090", json=taxonomy_record)
                m.post(config.TRACTION_URL, text="This is an error", status_code=422)

                assert instance.process(valid_create_labware_message) is True
                error_code.trigger.assert_called()

            mock_avro_encoder.assert_called_once_with(schema_registry, RABBITMQ_SUBJECT_CREATE_LABWARE_FEEDBACK)
            publisher.publish_message.assert_called_once()


def test_create_labware_processor_when_traction_sends_500(config, valid_create_labware_message, taxonomy_record):
    with patch("tol_lab_share.messages.output_feedback_message.AvroEncoderJson") as mock_avro_encoder:
        schema_registry = MagicMock()
        publisher = MagicMock()

        instance = CreateLabwareProcessor(schema_registry, publisher, config)

        with requests_mock.Mocker() as m:
            m.get(config.EBI_TAXONOMY_URL + "/10090", json=taxonomy_record)
            m.post(config.TRACTION_URL, text="This is an error", status_code=500)
            assert instance.process(valid_create_labware_message) is True

        mock_avro_encoder.assert_called_once_with(schema_registry, RABBITMQ_SUBJECT_CREATE_LABWARE_FEEDBACK)
        publisher.publish_message.assert_called_once()
