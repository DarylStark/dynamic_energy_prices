""" Module that contains the functions to update the prices in
    the database """

from database import DatabaseSession
from ep_database_model import GasPrice, PowerPrice
from ep_model.price import Price

from datetime import datetime
from pydantic import validate_arguments

from sqlalchemy import or_


@validate_arguments
def save_power_price(prices: list[Price]) -> None:
    """ Function to update power prices """

    with DatabaseSession(commit_on_end=True, expire_on_commit=False) as session:
        for price in prices:
            # Search this date and time in the database
            price_object = session.query(PowerPrice).filter(
                PowerPrice.date == price.date.isoformat(),
                PowerPrice.time == price.time
            ).first()

            if price_object:
                # Update the current object
                if price_object.price != price.price:
                    price_object.price = price.price
                    price_object.updated_on = datetime.now()
                continue

            # Create a new object
            price_object = PowerPrice(
                date=price.date,
                time=price.time,
                price=price.price,
                updated_on=datetime.now()
            )
            session.add(price_object)


@validate_arguments
def save_gas_price(prices: list[Price]) -> None:
    """ Function to update gas prices """

    with DatabaseSession(commit_on_end=True, expire_on_commit=False) as session:
        for price in prices:
            # Search this date and time in the database
            price_object = session.query(GasPrice).filter(
                GasPrice.date == price.date.isoformat(),
                GasPrice.time == price.time
            ).first()

            if price_object:
                # Update the current object
                if price_object.price != price.price:
                    price_object.price = price.price
                    price_object.updated_on = datetime.now()
                continue

            # Create a new object
            price_object = GasPrice(
                date=price.date,
                time=price.time,
                price=price.price,
                updated_on=datetime.now()
            )
            session.add(price_object)


@validate_arguments
def get_power_prices(start: datetime, end: datetime) -> list[Price] | None:
    """ Method to retrieve power prices from the database """

    start = start.replace(tzinfo=None)
    end = end.replace(tzinfo=None)

    with DatabaseSession(commit_on_end=True, expire_on_commit=False) as session:
        prices = session.query(PowerPrice)
        if prices.count() > 0:
            return [
                Price(
                    date=price.date,
                    time=price.time,
                    price=price.price
                ) for price in prices.all()
                if (datetime.combine(price.date, price.time) >= start and
                    datetime.combine(price.date, price.time) < end)
            ]

    # Nothing found
    return None
