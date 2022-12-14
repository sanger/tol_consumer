from unittest.mock import MagicMock, patch
from tol_lab_share.processors.create_labware_processor import CreateLabwareProcessor
from tol_lab_share.constants import RABBITMQ_SUBJECT_CREATE_LABWARE_FEEDBACK


def test_create_labware_processor(config):
    with patch("tol_lab_share.processors.create_labware_processor.AvroEncoderBinary") as mock_avro_encoder:
        schema_registry = MagicMock()
        assert CreateLabwareProcessor(schema_registry, MagicMock(), config) is not None

        mock_avro_encoder.assert_called_once_with(schema_registry, RABBITMQ_SUBJECT_CREATE_LABWARE_FEEDBACK)


def test_create_labware_processor_can_run_process(config, decoded_rabbit_message):
    with patch("tol_lab_share.processors.create_labware_processor.AvroEncoderBinary") as mock_avro_encoder:
        schema_registry = MagicMock()

        instance = CreateLabwareProcessor(schema_registry, MagicMock(), config)
        mock_avro_encoder.assert_called_once_with(schema_registry, RABBITMQ_SUBJECT_CREATE_LABWARE_FEEDBACK)

        assert instance.process(decoded_rabbit_message) == True
