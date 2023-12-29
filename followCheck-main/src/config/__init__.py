import json
import sys

from loguru import logger

from src.config.models import ConfigModel


with open("src/variables.json", mode="r", encoding="UTF-8") as file:
    raw_config = json.load(file)


config: ConfigModel = ConfigModel(**raw_config)


LOG_FORMAT = (
    "<magenta>AF CM</magenta> | "
    "<level>{level: <8}</level> | "
    "<italic><green>{time:YYYY-MM-DD HH:mm:ss}</green></italic> | "
    "{name}:{function}:{line} > <level>{message}</level>"
)

logger.remove()
logger.add(sys.stderr, format=LOG_FORMAT, level="INFO", enqueue=True, colorize=True)


LINKS_REGEX_PATTERN = r"(?:https?:\/\/)?(?:www\.)?vk\.(?:com|ru)\/([\w.-]+)"
HYPERLINKS_REGEX_PATTERN = r"\b((?:id|club)\d+)\|[^]]+"


__all__ = (
    "logger",
    "config",
    "LINKS_REGEX_PATTERN",
    "HYPERLINKS_REGEX_PATTERN",
)
