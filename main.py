import time
import sys
from importlib import import_module
from typing import Tuple, cast
import os
import logging
import logging.config
from lab_share_lib.rabbit.rabbit_stack import RabbitStack

def get_config(settings_module: str = ""):
    """Get the config for the app by importing a module named by an environment variable. This allows easy switching
    between environments and inheriting default config values.

    Arguments:
        settings_module (str, optional): the settings module to load. Defaults to "".

    Returns:
        Tuple[Config, str]: tuple with the config module loaded and available to use via `config.<param>` and the
        settings module used
    """
    try:
        if not settings_module:
            settings_module = os.environ["SETTINGS_MODULE"]

        config_module = import_module(settings_module)

        return config_module
    except KeyError as e:
        sys.exit(f"{e} required in environment variables for config.")


config = get_config("")
logging.config.dictConfig(config.LOGGING)
rabbit_stack = RabbitStack(config)

rabbit_stack.bring_stack_up()

while True:
    print("Running")
    time.sleep(5)
