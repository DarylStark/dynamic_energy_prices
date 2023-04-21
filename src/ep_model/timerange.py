""" Module with the data model for Energy Prices """

from pydantic import BaseModel

from .price import Price


class TimeRange(BaseModel):
    """ Model for EnergyPrices """
    start: Price | None = None
    end: Price | None = None
    sum: float = 0
    avg: float = 0
