#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Client for RPi meeting program."""

from os import getenv
from platform import python_version

import click
import colorlog
import requests
from dotenv import find_dotenv, load_dotenv

import utils

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


def setlevel(level, message, end):
    """Set meeting level."""
    data = {"level": level, "msg": message, "end": end}
    logger.info(f"Data: {data}")
    logger.info(f"Sending request to rpi server at {RPI_IP}:{RPI_PORT}")
    response = requests.post(f"http://{RPI_IP}:{RPI_PORT}/setlevel", json=data)
    logger.info(f"Response received from rpi server at {RPI_IP}:{RPI_PORT}")
    response.raise_for_status()
    print(f"Level set: {data}")
    return


def set_options(function):
    """Set options."""
    function = click.option(
        "-m",
        "--message",
        "message",
        help="add message",
    )(function)
    function = click.option(
        "-e",
        "--end",
        "end",
        help="add end time",
    )(function)
    return function


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option("", message=f"mclient 1.0.0 || Python {python_version()}")
def cli() -> None:
    """Meet client."""
    return


@cli.command()
@utils.verbosity
def get(verbosity):
    """Get current level."""
    utils.logconfig(verbosity)
    logger.info(f"Getting current level from rpi server at {RPI_IP}:{RPI_PORT}")
    response = requests.get(f"http://{RPI_IP}:{RPI_PORT}/getlevel")
    logger.info(f"Response received from rpi server at {RPI_IP}:{RPI_PORT}")
    print(response.text)
    return


@cli.command()
@set_options
@utils.verbosity
def low(message, end, verbosity):
    """Set low level."""
    utils.logconfig(verbosity)
    setlevel("low", message, end)
    return


@cli.command()
@set_options
@utils.verbosity
def med(message, end, verbosity):
    """Set medium level."""
    utils.logconfig(verbosity)
    setlevel("med", message, end)
    return


@cli.command()
@set_options
@utils.verbosity
def high(message, end, verbosity):
    """Set high level."""
    utils.logconfig(verbosity)
    setlevel("high", message, end)
    return


@cli.command()
@set_options
@utils.verbosity
def off(message, end, verbosity):
    """Turn off."""
    utils.logconfig(verbosity)
    setlevel("off", message, end)
    return


if __name__ == "__main__":
    cli()
