#!/usr/bin/python3

from os import getenv
from time import sleep

import board
import colorlog
import digitalio
import requests
from dotenv import find_dotenv, load_dotenv

from utils import logconfig

logger = colorlog.getLogger()


def blink(led):
    led.direction = digitalio.Direction.OUTPUT
    led.value = True
    sleep(1)
    led.value = False
    sleep(2)
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
            logger.info("Checking level")
            response = session.get(f"http://{RPI_IP}:{RPI_PORT}/getlevel")
            data = response.json()
            logger.info(f"Current level: {data}")
            if data["level"] == "off":
                sleep(5)
            else:
                led = leds[data["level"]]
                for x in range(3):
                    blink(led)
