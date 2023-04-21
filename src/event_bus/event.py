""" The object type for events """

from typing import Any
from pydantic import BaseModel, Field
from datetime import datetime


class Event(BaseModel):
    """ Class for Event objects """
    event: str
    raised_on: datetime = Field(default_factory=datetime.now)
    data: Any | None = None
