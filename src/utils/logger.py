"""Logging utilities for the project."""

from __future__ import annotations

import logging


def get_logger(name: str) -> logging.Logger:
    """Return a configured project logger.

    The function avoids adding duplicate handlers when called multiple times
    with the same logger name.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)s | %(module)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
