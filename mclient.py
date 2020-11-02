#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Client for RPi meeting program."""

import argparse
import sys

import colorlog
import requests

logger = colorlog.getLogger()


def getlevel():
    """Get current level."""
    logger.info("Getting current level from rpi server")
    response = requests.get("http://localhost:8080/getlevel")
    logger.info("Response received from rpi server")
    print(response.text)
    return


def setlevel(args):
    """Set meeting level."""
    level = args.level
    logger.info(f"Level requested: {level}")
    logger.info("Sending request to rpi server")
    response = requests.get(f"http://localhost:8080/setlevel/{level}")
    logger.info("Response received from rpi server")
    response.raise_for_status()
    print(f"Meeting level set: {level}")
    return


def logconfig(level="WARNING"):
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


def main(args):
    """Main."""
    if args.level == "get":
        getlevel()
    else:
        setlevel(args)


def menu(args):
    """CLI menu."""
    parser = argparse.ArgumentParser(prog="mclient", description="Meeting client")
    levels = ("get", "off", "low", "med", "high")
    parser.add_argument("level", default="med", choices=levels)
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
