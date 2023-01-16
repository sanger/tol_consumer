from unittest.mock import MagicMock, patch
from tol_lab_share.processors.create_labware_processor import CreateLabwareProcessor
from tol_lab_share.constants import RABBITMQ_SUBJECT_CREATE_LABWARE_FEEDBACK
import requests_mock


def test_create_labware_processor(config):
    schema_registry = MagicMock()
    assert CreateLabwareProcessor(schema_registry, MagicMock(), config) is not None


def test_create_labware_processor_can_run_process(
    config, valid_create_labware_message, mocked_response, taxonomy_record
):
    with patch("tol_lab_share.messages.output_feedback_message.AvroEncoderBinary") as mock_avro_encoder:
        schema_registry = MagicMock()
        publisher = MagicMock()

        instance = CreateLabwareProcessor(schema_registry, publisher, config)

        with requests_mock.Mocker() as m:
            m.get(config.EBI_TAXONOMY_URL + "/10090", json=taxonomy_record)
            m.post(config.TRACTION_URL, json=mocked_response)
            assert instance.process(valid_create_labware_message) is True

        mock_avro_encoder.assert_called_once_with(schema_registry, RABBITMQ_SUBJECT_CREATE_LABWARE_FEEDBACK)
        publisher.publish_message.assert_called_once()


def test_create_labware_processor_when_traction_sends_422(config, valid_create_labware_message, taxonomy_record):
    with patch("tol_lab_share.messages.output_feedback_message.AvroEncoderBinary") as mock_avro_encoder:
        schema_registry = MagicMock()
        publisher = MagicMock()

        instance = CreateLabwareProcessor(schema_registry, publisher, config)

        with requests_mock.Mocker() as m:
            m.get(config.EBI_TAXONOMY_URL + "/10090", json=taxonomy_record)
            m.post(config.TRACTION_URL, text="This is an error", status_code=422)

            assert instance.process(valid_create_labware_message) is True

        mock_avro_encoder.assert_called_once_with(schema_registry, RABBITMQ_SUBJECT_CREATE_LABWARE_FEEDBACK)
        publisher.publish_message.assert_called_once()


def test_create_labware_processor_when_traction_sends_500(config, valid_create_labware_message, taxonomy_record):
    with patch("tol_lab_share.messages.output_feedback_message.AvroEncoderBinary") as mock_avro_encoder:
        schema_registry = MagicMock()
        publisher = MagicMock()

        instance = CreateLabwareProcessor(schema_registry, publisher, config)

        with requests_mock.Mocker() as m:
            m.get(config.EBI_TAXONOMY_URL + "/10090", json=taxonomy_record)
            m.post(config.TRACTION_URL, text="This is an error", status_code=500)
            assert instance.process(valid_create_labware_message) is True

        mock_avro_encoder.assert_called_once_with(schema_registry, RABBITMQ_SUBJECT_CREATE_LABWARE_FEEDBACK)
        publisher.publish_message.assert_called_once()
