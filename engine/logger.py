# engine/logger.py

"""
Taylor NQ Logger

Application logging utilities.
"""

from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from config import LOG_DIR


LOG_FILE = LOG_DIR / "taylor_nq.log"


class Logger:

    _configured = False

    @classmethod
    def configure(cls):

        if cls._configured:
            return

        LOG_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        handler = RotatingFileHandler(
            LOG_FILE,
            maxBytes=5_000_000,
            backupCount=5,
            encoding="utf-8",
        )

        handler.setFormatter(formatter)

        root = logging.getLogger()

        root.setLevel(logging.INFO)

        root.addHandler(handler)

        cls._configured = True

    @staticmethod
    def info(message: str):
        logging.getLogger().info(message)

    @staticmethod
    def warning(message: str):
        logging.getLogger().warning(message)

    @staticmethod
    def error(message: str):
        logging.getLogger().error(message)

    @staticmethod
    def exception(message: str):
        logging.getLogger().exception(message)

    @staticmethod
    def debug(message: str):
        logging.getLogger().debug(message)
