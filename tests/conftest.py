import pytest
import logging
import logging.config
from tol_lab_share.helpers import get_config

CONFIG = get_config("tol_lab_share.config.test")
logging.config.dictConfig(CONFIG.LOGGING)

@pytest.fixture
def config():
    return CONFIG

