import logging
from tol_lab_share.messages.output_feedback_message import OutputFeedbackMessage
from tol_lab_share.messages.output_traction_message import OutputTractionMessage
from typing import Optional, Any
from functools import cached_property
from tol_lab_share.data_resolvers.data_resolver_state_machine import DataResolverStateMachine
from tol_lab_share.data_resolvers.data_resolver_interface import DataResolverInterface

logger = logging.getLogger(__name__)


class DataResolver(DataResolverInterface):
    def __init__(self, instance):
        self._instance = instance
        self._errors = []
        self._value = None
        self.state = DataResolverStateMachine()

    def validate(self):
        logger.debug("DataResolver::validate")
        self.state.performing_validation()
        result = self._instance.validate()
        if result:
            self.state.validation_passed()
        else:
            self.state.validation_failed()
        return result

    def resolve(self):
        logger.debug("DataResolver::resolve")
        self.state.request_resolution()

        self._instance.resolve()

        self.state.resolution_successful()

    @property
    def errors(self) -> Any:
        return self._instance.errors

    @cached_property
    def value(self) -> Optional[Any]:
        logger.debug("DataResolver::value")
        self.state.retrieve_value()
        return self._instance.value

    def add_to_feedback_message(self, feedback_message: OutputFeedbackMessage) -> None:
        logger.debug("DataResolver::add_to_feedback_message")
        self.state.retrieve_feedback()
        feedback_message.operation_was_error_free = self.state.is_resolved and len(self.errors) == 0
        self._instance.add_to_feedback_message(feedback_message)

    def add_to_traction_message(self, traction_message: OutputTractionMessage) -> None:
        logger.debug("DataResolver::add_to_traction_message")
        self.state.retrieve_feedback()
        self._instance.add_to_traction_message(traction_message)
