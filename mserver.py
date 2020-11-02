#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Server for RPi meeting program."""

from bottle import get, run
import colorlog

import mlights

logger = colorlog.getLogger()


@get("/<level>")
def meeting(level):
    """Set LED and message to specified level."""
    logger.info("Turning on light and setting message on display.")
    colors = {"low": "green", "med": "yellow", "high": "red"}
    result = mlights.blink(colors[level])
    return result


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
