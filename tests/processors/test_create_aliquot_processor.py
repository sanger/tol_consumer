from unittest.mock import MagicMock, patch

# import pytest
# import requests_mock

from lab_share_lib.processing.base_processor import BaseProcessor


# from tol_lab_share.constants import RABBITMQ_SUBJECT_CREATE_ALIQUOT_FEEDBACK
# from tol_lab_share.messages.rabbit.consumed import CreateAliquotMessage
# from tol_lab_share.messages.rabbit.published import CreateAliquotFeedbackMessage
from tol_lab_share.processors.create_aliquot_processor import CreateAliquotProcessor


class TestCreateAliquotProcessor:
    def test_is_subclass_of_base_processor(self):
        assert issubclass(CreateAliquotProcessor, BaseProcessor)

    def test_can_be_initialised(self, config):
        schema_registry = MagicMock()
        assert CreateAliquotProcessor(schema_registry, MagicMock(), config) is not None

    def test_instantiate_returns_instance(self, config):
        instance = CreateAliquotProcessor.instantiate(MagicMock(), MagicMock(), config)
        assert isinstance(instance, CreateAliquotProcessor)

    def test_instantiate_passes_arguments_to_init(self, config):
        schema_registry = MagicMock()
        basic_publisher = MagicMock()

        with patch("tol_lab_share.processors.create_aliquot_processor.CreateAliquotProcessor.__init__") as init_mock:
            init_mock.return_value = None
            CreateAliquotProcessor.instantiate(schema_registry, basic_publisher, config)

        init_mock.assert_called_with(schema_registry, basic_publisher, config)
