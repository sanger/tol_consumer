from unittest.mock import MagicMock, patch
from tol_lab_share.processors.create_labware_processor import CreateLabwareProcessor
from tol_lab_share.constants import RABBITMQ_SUBJECT_CREATE_LABWARE_FEEDBACK


def test_create_labware_processor(config):
    with patch("tol_lab_share.processors.create_labware_processor.AvroEncoder") as mock_avro_encoder:
        schema_registry = MagicMock()
        assert CreateLabwareProcessor(schema_registry, MagicMock(), config) is not None

        mock_avro_encoder.assert_called_once_with(schema_registry, RABBITMQ_SUBJECT_CREATE_LABWARE_FEEDBACK)
