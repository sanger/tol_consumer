import sys
from importlib import import_module
import os
from types import ModuleType


def get_config(settings_module: str = "") -> ModuleType:
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
            settings_module = os.getenv("SETTINGS_MODULE", "tol_lab_share.config.defaults")

        config_module = import_module(settings_module)

        return config_module
    except KeyError as e:
        sys.exit(f"{e} required in environment variables for config.")
