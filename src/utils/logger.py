"""
logging handling module to create custom and particular loggers.
"""

import logging
from typing import Optional
from src.settings import settings

logging.basicConfig(format=settings.logging_format, style="{")


def get_logger(
    name: Optional[str] = None, log_level: Optional[str] = settings.log_level
) -> logging.Logger:
    """
    get a logger object.

    Args:
        name (:obj:`str`, optional): Specify a name if you want
            to retrieve a logger which is a child of
            LinkedinAPI logger.
        log_level (:obj:`str`, optional): Specify the log level
            for this particular logger.

    Returns:
        The LinkedinAPI logger, or one of its children.
    """

    # create logger
    _logger_name = f"LinkedinAPI"
    if name:
        _logger_name += f".{name}"

    # create logger
    logger = logging.getLogger(name=_logger_name)
    # set log level
    if not log_level == None:
        logger.setLevel(log_level)
    logging.debug(f"logger created {logger}")

    return logger
