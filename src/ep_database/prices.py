""" Module that contains the functions to update the prices in
    the database """

from database import DatabaseSession
from ep_database_model import GasPrice, PowerPrice
from dataclasses import dataclass

from datetime import date, time, datetime


@dataclass
class PriceEnergy:
    """ Model for EnergyPrices """
    date: date
    time: time
    price: float


def update_gas_price(prices: list[PriceEnergy]) -> None:
    """ Function to update gas prices """

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


def update_power_price() -> None:
    """ Function to update power prices """
    pass
