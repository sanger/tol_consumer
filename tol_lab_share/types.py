from types import ModuleType
from typing import Dict, Any


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

    # RedPanda
    REDPANDA_BASE_URI: str
    REDPANDA_API_KEY: str

    PROCESSORS: Dict[str, str]
