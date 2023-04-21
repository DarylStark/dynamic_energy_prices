""" Module with functions for the metrics """

from ep_database.prices import get_power_prices
from event_bus import Event
from energy_prices.aggregators import get_cheapest_successive_hours

import datetime
from zoneinfo import ZoneInfo

from config_loader import ConfigLoader


def get_cheapest_time_blocks(event: Event) -> None:
    """ Method that gets specific blocks of 'chepeast times' """

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

    pass

    # Get the blocks
    # TODO: Implement
