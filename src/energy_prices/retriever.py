""" Module that contains the functions to retrieve the data from
    the API """


import logging
import urllib.parse
from datetime import datetime, timedelta, date, time
from time import sleep

import requests

from config_loader import ConfigLoader
from ep_database.prices import update_gas_price, PriceEnergy


def data_retriever() -> None:
    """ Method that runs in the background and retrieves the data
        as soon as it is needed """

    # Create a logger for the My REST API package
    logger = logging.getLogger('retriever')

    datetime_last_check = datetime(
        year=2022, month=1, day=1, hour=0, minute=0, second=0)

    # Get the max age in minutes
    max_age_in_min = ConfigLoader.config['retrieval']['max_age_in_minutes']

    # Done with the initialization phase
    logger.info('Application initialized')

    # Main loop
    while True:
        # Check if the age of the data is too old
        diff: timedelta = datetime.now() - datetime_last_check
        age = diff.total_seconds() / 60
        if age > max_age_in_min:
            logger.info('Information is too old and should be updated!')

            # Start the process to update the prices
            update_prices()
            logger.info('Prices are updated!')
            datetime_last_check = datetime.now()

        # Sleep 1 second so we don't overload the script
        sleep(1)


def update_prices() -> None:
    """ The method to sync the prices """

    url_template = ConfigLoader.config['retrieval']['url_template']

    logger = logging.getLogger('sync_prices')
    logger.info('Syncing prices')

    # Create start time strings
    start = datetime.now() - timedelta(hours=4)
    start_date = start.strftime('%Y-%m-%d')
    start_time = start.strftime('%H:00:00')

    # Create end time strings
    end = datetime.now() + timedelta(hours=48)
    end_date = end.strftime('%Y-%m-%d')
    end_time = end.strftime('%H:59:59')

    # Generate the Base URL
    base_url = url_template
    base_url = base_url.replace(
        '{{ start_date }}', urllib.parse.quote(start_date))
    base_url = base_url.replace(
        '{{ start_time }}', urllib.parse.quote(start_time))
    base_url = base_url.replace('{{ end_date }}', urllib.parse.quote(end_date))
    base_url = base_url.replace('{{ end_time }}', urllib.parse.quote(end_time))

    # Generate the URL for power
    power_url = base_url.replace('{{ type }}', '1')

    # Generate the URL for gas
    gas_url = base_url.replace('{{ type }}', '2')

    # Retrieve the data
    logger.info('Retrieving power prices')
    power_prices_from_api = requests.get(
        url=power_url,
        timeout=30).json()

    # Convert to dict object
    power_prices = [
        PriceEnergy(
            date=date.fromisoformat(price['readingDate'].split('T')[0]),
            time=time.fromisoformat(price['readingDate'].split('T')[1][0:5]),
            price=price['price']
        )
        for price in power_prices_from_api['Prices']
    ]

    # Update the database
    update_gas_price(power_prices)

    logger.info('Done syncing prices')
