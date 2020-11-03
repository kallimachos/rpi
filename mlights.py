#!/usr/bin/python3

import json
import time
from os import getenv

import board
import colorlog
import digitalio
import requests
from dotenv import find_dotenv, load_dotenv


logger = colorlog.getLogger()


def blink(led):
    led.direction = digitalio.Direction.OUTPUT
    led.value = True
    time.sleep(1.0)
    led.value = False
    time.sleep(2.0)
    return


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
    load_dotenv(find_dotenv())
    RPI_IP = getenv("RPI_IP")
    RPI_PORT = getenv("RPI_PORT")
    leds = {
        "low": digitalio.DigitalInOut(board.D16),  # green
        "med": digitalio.DigitalInOut(board.D20),  # yellow
        "high": digitalio.DigitalInOut(board.D21),  # red
    }
    with requests.Session() as session:
        while True:
            logger.debug("Checking level")
            response = session.get(f"http://{RPI_IP}:{RPI_PORT}/getlevel")
            data = response.json()
            logger.debug(f"Current level: {data}")
            if data["level"] == "off":
                time.sleep(5.0)
            else:
                led = leds[data["level"]]
                for x in range(3):
                    blink(led)
