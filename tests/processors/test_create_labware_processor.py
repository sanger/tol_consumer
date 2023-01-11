from unittest.mock import MagicMock, patch
from tol_lab_share.processors.create_labware_processor import CreateLabwareProcessor
from tol_lab_share.constants import RABBITMQ_SUBJECT_CREATE_LABWARE_FEEDBACK
import requests_mock  # type: ignore
import requests
from pytest import raises


def test_create_labware_processor(config):
    with patch("tol_lab_share.processors.create_labware_processor.AvroEncoderBinary") as mock_avro_encoder:
        schema_registry = MagicMock()
        assert CreateLabwareProcessor(schema_registry, MagicMock(), config) is not None

        mock_avro_encoder.assert_called_once_with(schema_registry, RABBITMQ_SUBJECT_CREATE_LABWARE_FEEDBACK)


def test_create_labware_processor_can_run_process(config, valid_create_labware_message, mocked_response):
    with patch("tol_lab_share.processors.create_labware_processor.AvroEncoderBinary") as mock_avro_encoder:
        schema_registry = MagicMock()

        instance = CreateLabwareProcessor(schema_registry, MagicMock(), config)
        mock_avro_encoder.assert_called_once_with(schema_registry, RABBITMQ_SUBJECT_CREATE_LABWARE_FEEDBACK)

        with requests_mock.Mocker() as m:
            m.post(config.TRACTION_URL, json=mocked_response)
            assert instance.process(valid_create_labware_message) is True


def test_create_labware_processor_when_traction_sends_422(config, valid_create_labware_message):
    with patch("tol_lab_share.processors.create_labware_processor.AvroEncoderBinary") as mock_avro_encoder:
        schema_registry = MagicMock()

        instance = CreateLabwareProcessor(schema_registry, MagicMock(), config)
        mock_avro_encoder.assert_called_once_with(schema_registry, RABBITMQ_SUBJECT_CREATE_LABWARE_FEEDBACK)

        with requests_mock.Mocker() as m:
            m.post(config.TRACTION_URL, text="This is an error", status_code=422)

            with raises(requests.exceptions.HTTPError):
                instance.process(valid_create_labware_message)


def test_create_labware_processor_when_traction_sends_500(config, valid_create_labware_message):
    with patch("tol_lab_share.processors.create_labware_processor.AvroEncoderBinary") as mock_avro_encoder:
        schema_registry = MagicMock()

        instance = CreateLabwareProcessor(schema_registry, MagicMock(), config)
        mock_avro_encoder.assert_called_once_with(schema_registry, RABBITMQ_SUBJECT_CREATE_LABWARE_FEEDBACK)

        with requests_mock.Mocker() as m:
            m.post(config.TRACTION_URL, text="This is an error", status_code=500)
            with raises(requests.exceptions.HTTPError):
                instance.process(valid_create_labware_message)
