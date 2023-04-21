""" Module with the data model for Energy Prices """

from datetime import date, time

from pydantic import BaseModel


class Price(BaseModel):
    """ Model for EnergyPrices """
    date: date
    time: time
    price: float
