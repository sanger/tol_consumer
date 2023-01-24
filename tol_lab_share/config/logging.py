from typing import Any, Dict

DEFAULT_LOGGING_LEVEL = "INFO"

LOGGING: Dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "colored": {
            "style": "{",
            "()": "colorlog.ColoredFormatter",
            "format": "{asctime:<15} {name:<25}:{lineno:<3} {log_color}{levelname:<7} {message}",
        },
        "colored_dev": {
            "style": "{",
            "()": "colorlog.ColoredFormatter",
            "format": "{asctime:<15} {relative_path_and_lineno:<35} {log_color}{levelname:<7} {message}",
        },
        "verbose": {
            "style": "{",
            "format": "{asctime:<15} {name:<45}:{lineno:<3} {levelname:<7} {message}",
        },
    },
    "handlers": {
        "colored_stream": {
            "level": DEFAULT_LOGGING_LEVEL,
            "class": "colorlog.StreamHandler",
            "formatter": "colored",
        },
        "console": {
            "level": DEFAULT_LOGGING_LEVEL,
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "tol_lab_share": {
            "handlers": ["console"],
            "level": DEFAULT_LOGGING_LEVEL,
            "propagate": True,
        },
        "lab_share_lib": {
            "handlers": ["console"],
            "level": DEFAULT_LOGGING_LEVEL,
            "propagate": True,
        },
        "rabbit_messages": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": True,
        },
    },
}
