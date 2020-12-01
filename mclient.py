#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Client for RPi meeting program."""

import argparse
import sys
from os import getenv

import colorlog
import requests
from dotenv import find_dotenv, load_dotenv

from utils import logconfig

logger = colorlog.getLogger()
load_dotenv(find_dotenv())
RPI_IP = getenv("RPI_IP")
RPI_PORT = getenv("RPI_PORT")


def getlevel():
    """Get current level."""
    logger.info(f"Getting current level from rpi server at {RPI_IP}:{RPI_PORT}")
    response = requests.get(f"http://{RPI_IP}:{RPI_PORT}/getlevel")
    logger.info(f"Response received from rpi server at {RPI_IP}:{RPI_PORT}")
    print(response.text)
    return


def setlevel(args):
    """Set meeting level."""
    data = {"level": args.level, "msg": " ".join(args.message), "end": " ".join(args.end)}
    logger.info(f"Data: {data}")
    logger.info(f"Sending request to rpi server at {RPI_IP}:{RPI_PORT}")
    response = requests.post(f"http://{RPI_IP}:{RPI_PORT}/setlevel", json=data)
    logger.info(f"Response received from rpi server at {RPI_IP}:{RPI_PORT}")
    response.raise_for_status()
    print(f"Level set: {data}")
    return


def main(args):
    """Main."""
    if args.level == "get":
        getlevel()
    else:
        setlevel(args)
    return


def menu(args):
    """CLI menu."""
    parser = argparse.ArgumentParser(prog="mclient", description="Meeting client")
    levels = ("get", "off", "low", "med", "high")
    parser.add_argument("level", default="med", choices=levels)
    parser.add_argument(
        "-m", "--message", type=str, nargs="+", default=[], help="Message to display"
    )
    parser.add_argument("-e", "--end", type=str, nargs="+", default=[], help="End time")
    parser.add_argument(
        "-v", "--verbose", action="count", default=0, help="increase verbosity (-v, -vv)"
    )
    arguments = parser.parse_args(args)
    if arguments.verbose == 1:
        logconfig("INFO")
    elif arguments.verbose == 2:
        logconfig("DEBUG")
    logger.debug(f"args: {arguments}")
    return arguments


if __name__ == "__main__":
    args = menu(sys.argv[1:])
    main(args)
