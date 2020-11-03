#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Server for RPi meeting program."""

import json
from os import getenv

import colorlog
from bottle import get, post, request, run
from dotenv import find_dotenv, load_dotenv

from utils import logconfig

logger = colorlog.getLogger()
data = json.dumps({"level": "off", "msg": "", "end": ""})


@post("/setlevel")
def setlevel():
    """Set level, message, and end time."""
    global data
    data = request.json
    logger.info(f"Level set: {data}.")
    return


@get("/getlevel")
def getlevel():
    """Get level and message."""
    logger.info("Returning level, message, and end time.")
    return data


if __name__ == "__main__":
    logconfig()
    load_dotenv(find_dotenv())
    RPI_IP = getenv("RPI_IP")
    RPI_PORT = getenv("RPI_PORT")
    run(host=RPI_IP, port=RPI_PORT, debug=False, reloader=False)
