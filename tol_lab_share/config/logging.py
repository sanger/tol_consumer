from typing import Any, Dict

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
            "level": "DEBUG",
            "class": "colorlog.StreamHandler",
            "formatter": "colored",
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "lab_share_lib": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": True,
        },
    },
}
