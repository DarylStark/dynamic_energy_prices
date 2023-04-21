""" Module that contains the functions to retrieve the data from
    the API """


import logging
import urllib.parse
from datetime import date, datetime, time, timedelta
from time import sleep

import requests

from config_loader import ConfigLoader
from ep_database.prices import Price, save_gas_price, save_power_price

from .bus import bus


def data_retriever() -> None:
    """ Method that runs in the background and retrieves the data
        as soon as it is needed """

    # Create a logger for the My REST API package
    logger = logging.getLogger('data_retriever')

    datetime_last_check = datetime(
        year=2022, month=1, day=1, hour=0, minute=0, second=0)

    # Get the max age in minutes
    max_age_in_min = ConfigLoader.config['retrieval']['max_age_in_minutes']

    # Done with the initialization phase
    logger.info('Application initialized')

    bus.emit('data_retriever_thread_initialized')

    # Main loop
    while True:
        # Check if the age of the data is too old
        diff: timedelta = datetime.now() - datetime_last_check
        age = diff.total_seconds() / 60
        if age > max_age_in_min:
            bus.emit('updating_prices_from_retriever')
            logger.info('Information is too old and should be updated!')

            # Create the time objects for the update
            start = datetime.now() - timedelta(hours=4)
            end = datetime.now() + timedelta(hours=48)

            # Start the process to update the prices
            update_prices(start, end)
            logger.info('Prices are updated!')
            datetime_last_check = datetime.now()

        # Sleep 1 second so we don't overload the script
        sleep(1)


def get_date_from_api(start: datetime, end: datetime, type: str) -> dict:
    """ Function to retrieve data from a specific URL """

    logger = logging.getLogger('get_date_from_api')

    # Get the URL template
    url = ConfigLoader.config['retrieval']['url_template']

    # Generate the Base URL
    url = url.replace('{{ start_date }}',
                      urllib.parse.quote(start.strftime('%Y-%m-%d')))
    url = url.replace('{{ start_time }}',
                      urllib.parse.quote(start.strftime('%H:00:00')))
    url = url.replace('{{ end_date }}',
                      urllib.parse.quote(end.strftime('%Y-%m-%d')))
    url = url.replace('{{ end_time }}',
                      urllib.parse.quote(end.strftime('%H:59:59')))

    # Generate the URL for power
    power_url = url.replace('{{ type }}', type)

    # Retrieve the data
    logger.info(f'Retrieving prices from URL "{url}"')
    return requests.get(
        url=power_url,
        timeout=30).json()


def update_prices(start: datetime, end: datetime) -> None:
    """ The function to sync the prices """

    logger = logging.getLogger('sync_prices')
    logger.info('Syncing prices')

    # Update the correct fields
    update_power_prices(start, end)
    update_gas_prices(start, end)

    logger.info('Done syncing prices')
    bus.emit('prices_synced')


def update_power_prices(start: datetime, end: datetime) -> None:
    """ Function to update energy prices in the database """

    logger = logging.getLogger('update_energy_price')
    logger.info('Updating power prices')

    # Get the power prices
    power_prices_from_api = get_date_from_api(start, end, '1')

    # Convert to the correct object types
    power_prices = [
        Price(
            date=date.fromisoformat(price['readingDate'].split('T')[0]),
            time=time.fromisoformat(price['readingDate'].split('T')[1][0:5]),
            price=price['price']
        )
        for price in power_prices_from_api['Prices']
    ]

    # Save it to the database
    save_power_price(power_prices)
    bus.emit('power_prices_synced')


def update_gas_prices(start: datetime, end: datetime) -> None:
    """ Function to update gas prices in the database """

    logger = logging.getLogger('update_gas_prices')
    logger.info('Updating gas prices')

    # Get the power prices
    gas_prices_from_api = get_date_from_api(start, end, '4')

    # Convert to the correct object types
    gas_prices = [
        Price(
            date=date.fromisoformat(price['readingDate'].split('T')[0]),
            time=time.fromisoformat(price['readingDate'].split('T')[1][0:5]),
            price=price['price']
        )
        for price in gas_prices_from_api['Prices']
    ]

    # Save it to the database
    save_gas_price(gas_prices)
    bus.emit('gas_prices_synced')
