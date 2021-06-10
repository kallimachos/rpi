#!/usr/bin/python3

import click
import colorlog

logger = colorlog.getLogger()


def verbosity(function):
    """Verbosity options."""
    function = click.option(
        "-v",
        "--verbosity",
        count=True,
        default=0,
        help="Increase verbosity (-v, -vv, -vvv, -vvvv).",
    )(function)
    return function


def logconfig(verbosity: int = 0) -> str:
    """
    Set logging configuration.

    0 - CRITICAL: Program success/fail message
    1 - ERROR:    Item Fail/error messages
    2 - WARNING:  Item Warning messages
    3 - INFO:     Item Info messages
    4 - DEBUG:    Debug messages

    """
    logfmt = "%(log_color)s%(levelname)-8s %(message)s"
    if verbosity == 1:
        level = "ERROR"
    elif verbosity == 2:
        level = "WARNING"
    elif verbosity == 3:
        level = "INFO"
    elif verbosity >= 4:
        level = "DEBUG"
        logfmt = "%(log_color)s%(levelname)-8s [%(filename)s:%(funcName)s:%(lineno)d] %(message)s"
    else:
        level = "CRITICAL"
    handler = colorlog.StreamHandler()
    handler.setFormatter(colorlog.ColoredFormatter(logfmt))
    logger.addHandler(handler)
    logger.setLevel(level)
    colorlog.getLogger("googleapiclient").setLevel("ERROR")  # hide warnings from this module
    return logger.level
