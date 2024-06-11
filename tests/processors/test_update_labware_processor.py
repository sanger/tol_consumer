from unittest.mock import MagicMock, patch

from lab_share_lib.processing.base_processor import BaseProcessor
from tol_lab_share.processors.update_labware_processor import UpdateLabwareProcessor
from tol_lab_share.constants import RABBITMQ_SUBJECT_UPDATE_LABWARE_FEEDBACK


class TestUpdateLabwareProcessor:
    def test_is_subclass_of_base_processor(self):
        assert issubclass(UpdateLabwareProcessor, BaseProcessor)

    def test_instantiate_returns_instance(self, config):
        instance = UpdateLabwareProcessor.instantiate(MagicMock(), MagicMock(), config)
        assert isinstance(instance, UpdateLabwareProcessor)

    def test_calls_avro_encoder(self, config):
        with patch("tol_lab_share.processors.update_labware_processor.AvroEncoderBinary") as mock_avro_encoder:
            schema_registry = MagicMock()
            assert UpdateLabwareProcessor(schema_registry, MagicMock(), config) is not None

            mock_avro_encoder.assert_called_once_with(schema_registry, RABBITMQ_SUBJECT_UPDATE_LABWARE_FEEDBACK)
