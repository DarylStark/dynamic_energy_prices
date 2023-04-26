""" Module with functions for the metrics """

import time

from flask import Config
from ep_database.prices import get_power_prices
from event_bus import Event
from energy_prices.aggregators import get_cheapest_successive_hours

import datetime
from zoneinfo import ZoneInfo

from config_loader import ConfigLoader

import requests
import logging


def get_cheapest_time_blocks(event: Event) -> None:
    """ Method that gets specific blocks of 'chepeast times' """

    logger = logging.getLogger('get_cheapest_time_blocks')

    # Get a local timezone object
    local_timezone = ZoneInfo(ConfigLoader.config['timezone'])
    utc_timezone = ZoneInfo('UTC')

    # Get the datetime objects in UTC
    today = datetime.datetime.utcnow().astimezone(local_timezone)
    tomorrow = today + datetime.timedelta(days=1)

    # Set everything to zero
    today = today.replace(hour=0, minute=0, second=0, microsecond=0)
    tomorrow = tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)

    # Get the objects in UTC
    today = today.astimezone(utc_timezone)
    tomorrow = tomorrow.astimezone(utc_timezone)

    # Get the prices
    prices_today = get_power_prices(today, tomorrow)
    prices_tomorrow = get_power_prices(
        tomorrow, tomorrow + datetime.timedelta(hours=24))

    if prices_today is None or prices_tomorrow is None:
        return

    # Get the blocks
    chepeast_blocks = {
        'today_1': get_cheapest_successive_hours(prices_today, 1),
        'today_2': get_cheapest_successive_hours(prices_today, 2),
        'today_3': get_cheapest_successive_hours(prices_today, 3),
        'today_4': get_cheapest_successive_hours(prices_today, 4),
        'tomorrow_1': get_cheapest_successive_hours(prices_tomorrow, 1),
        'tomorrow_2': get_cheapest_successive_hours(prices_tomorrow, 2),
        'tomorrow_3': get_cheapest_successive_hours(prices_tomorrow, 3),
        'tomorrow_4': get_cheapest_successive_hours(prices_tomorrow, 4)
    }

    # Send the blocks to HomeAssistant
    for key, value in chepeast_blocks.items():
        entity_update = requests.post(
            url=f'{ConfigLoader.config["homeassistant"]["url"]}/api/states/input_datetime.energy_cheapest_{key}_time',
            headers={
                'Authorization': f'Bearer {ConfigLoader.config["homeassistant"]["token"]}',
                'Content-Type': 'application/json'
            },
            json={
                'state': value.start.time.strftime('%H:%M:%S')
            },
            verify=False,
            timeout=30
        )
        if entity_update.status_code != 200:
            logger.error(
                f'Error while updating Home Assistant: {entity_update.status_code}')

    pass
