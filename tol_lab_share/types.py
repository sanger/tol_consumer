from types import ModuleType
from typing import Dict, Any, Literal


class Config(ModuleType):
    """ModuleType class for the app config."""

    LOGGING: Dict[str, Any]

    # RabbitMQ
    RABBITMQ_HOST: str
    RABBITMQ_SSL: bool
    RABBITMQ_PORT: int
    RABBITMQ_USERNAME: str
    RABBITMQ_PASSWORD: str
    RABBITMQ_VHOST: str
    RABBITMQ_CRUD_QUEUE: str
    RABBITMQ_FEEDBACK_EXCHANGE: str
    RABBITMQ_PUBLISH_RETRY_DELAY: int
    RABBITMQ_PUBLISH_RETRIES: int
    SELECTED_ENCODER_FOR_FEEDBACK_MESSAGE: Literal["json", "binary"]

    # RedPanda
    REDPANDA_BASE_URI: str
    REDPANDA_API_KEY: str

    PROCESSORS: Dict[str, str]

    CERTIFICATES_VALIDATION_ENABLED: bool
    TRACTION_URL: str
    EBI_TAXONOMY_URL: str
    LOCALHOST: str
    ROOT_PASSWORD: str
