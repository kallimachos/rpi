#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Print weather."""

from datetime import datetime
from os import getenv
from pprint import pprint

from dotenv import find_dotenv, load_dotenv
from requests import get

load_dotenv(find_dotenv())
APP_ID = getenv("APP_ID")


def convert_timestamp(timestamp):
    """Return a nice date and time string in local timezone."""
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")


if __name__ == "__main__":
    api = "http://api.openweathermap.org/data/2.5/weather?q="
    query = f"Brisbane,AU&units=metric&appid={APP_ID}"

    api = "http://api.openweathermap.org/data/2.5/onecall?"
    query = f"lat=-27.47&lon=153.03&units=metric&appid={APP_ID}"

    r = get(api + query)
    json = r.json()
    current = {
        "date": datetime.fromtimestamp(json["current"]["dt"]),
        "feels_like": json["current"]["feels_like"],
        "humidity": json["current"]["humidity"],
        "temp": json["current"]["temp"],
        "dew_point": json["current"]["dew_point"],
        "wind_speed": json["current"]["wind_speed"],  # * 3.6,
        "sunrise": datetime.fromtimestamp(json["current"]["sunrise"]),
        "sunset": datetime.fromtimestamp(json["current"]["sunset"]),
        "weather": json["current"]["weather"][0]["description"],
    }
    pprint(current)
