#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Server for RPi meeting program."""

from bottle import get, run
import colorlog
from time import sleep

logger = colorlog.getLogger()
level = {"off": "None"}

@get("/setlevel/<newlevel>")
def setlevel(newlevel):
    """Set level and message."""
    levels = {"off": "None", "low": "green", "med": "yellow", "high": "red"}
    logger.info(f"Setting level to {newlevel}:{levels[newlevel]}.")
    global level
    level = {newlevel: levels[newlevel]}
    logger.info(f"Level set to {level}.")
    return


@get("/getlevel")
def getlevel():
    """Get level and message."""
    logger.info("Getting level and message.")
    return level


def logconfig(level="DEBUG"):
    """Set logging configuration."""
    handler = colorlog.StreamHandler()
    handler.setFormatter(
        colorlog.ColoredFormatter(
            "%(log_color)s%(levelname)-8s [%(filename)s:%(funcName)s:%(lineno)d] %(message)s"
        )
    )
    logger.addHandler(handler)
    logger.setLevel(level)
    logger.debug(f"Logging set to {level}")
    return


if __name__ == "__main__":
    logconfig()
    run(host="localhost", port=8080, debug=True, reloader=True)
