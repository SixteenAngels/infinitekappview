from __future__ import annotations

import logging
import sys
from loguru import logger
from core.config import settings


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno
        logger.bind(module=record.module).opt(exception=record.exc_info).log(level, record.getMessage())


def configure_logging() -> None:
    logging_root = logging.getLogger()
    for h in list(logging_root.handlers):
        logging_root.removeHandler(h)
    logging_root.handlers = [InterceptHandler()]
    logger.remove()
    logger.add(sys.stderr, level=settings.LOG_LEVEL, backtrace=True, diagnose=False)
