#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Server for RPi meeting program."""

import json
import logging
from os import getenv

from bottle import get, post, request, run
from dotenv import find_dotenv, load_dotenv

data = json.dumps({"level": "off", "msg": "", "end": ""})


@post("/setlevel")
def setlevel():
    """Set level, message, and end time."""
    global data
    data = request.json
    logging.info(f"Level set: {data}.")
    return


@get("/getlevel")
def getlevel():
    """Get level and message."""
    logging.info("Returning level, message, and end time.")
    return data


if __name__ == "__main__":
    logging.basicConfig(filename="/home/pi/mserver.log", level=logging.WARN)
    load_dotenv(find_dotenv())
    RPI_IP = getenv("RPI_IP")
    RPI_PORT = getenv("RPI_PORT")
    run(host=RPI_IP, port=RPI_PORT, debug=False, reloader=False)
