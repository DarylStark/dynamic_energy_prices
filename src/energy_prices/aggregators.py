""" Function that contains aggregators """

from pydantic import validate_arguments
from ep_model.price import Price
from ep_model.timerange import TimeRange


@validate_arguments
def get_cheapest_successive_hours(
        prices: list[Price],
        successive_hours: int) -> TimeRange | None:
    """ Function to find the cheapest hours in a range"""

    if len(prices) < successive_hours or successive_hours <= 0:
        return None

    # Create a return object
    lowest = TimeRange(sum=999999)

    # Loop through the hours and find the cheapest range
    for index in range(0, len(prices) - successive_hours):
        timerange_price: float = 0
        for subindex in range(0, successive_hours):
            timerange_price += prices[index + subindex].price
        if timerange_price < lowest.sum:
            lowest.start = prices[index]
            lowest.end = prices[index + (successive_hours - 1)]
            lowest.sum = timerange_price
            lowest.avg = timerange_price / successive_hours

    # Return the timerange
    return lowest
