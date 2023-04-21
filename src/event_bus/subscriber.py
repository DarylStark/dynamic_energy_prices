""" The object type for subscribers """


from typing import Callable
from pydantic import BaseModel


class Subscriber(BaseModel):
    """ Class for Subscriber objects """
    events: list[str]
    func: Callable
    args: dict = dict()
