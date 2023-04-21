""" Package that contains the EventBus class """

from logging import getLogger
from typing import Any, Callable
from .event import Event
from .subscriber import Subscriber


class EventBus:
    """ A class that can be used to initialize a eventbus object """

    def __init__(self, name: str | None = 'event_bus'):
        """ Initializer class """
        self.logger = getLogger(f'event_bus_{name}')
        self.subscribers: dict[str, list[Subscriber]] = {}

    def subscribe(self, events: list[str] | str, func: Callable, args: dict | None = None) -> Subscriber:
        """ Subscribe a callable """

        # Convert the events to a list, if needed
        if type(events) is str:
            events = [events]

        # Create a Subscriber object
        subscriber_object = Subscriber(
            events=events,
            func=func
        )

        # Update the subscription list
        for event in events:
            if event in self.subscribers:
                self.subscribers[event].append(subscriber_object)
                continue
            self.subscribers[event] = [subscriber_object]

        # Retrun the created object
        return subscriber_object

    def emit(self, event: str, data: Any = None) -> Event:
        """ Method to emit a event """

        self.logger.debug(f'Event emitted: "{event}"')

        # Create a Event object
        event_object = Event(event=event, data=data)

        # Loop through the subscriptions for this event
        subscriptions = self.subscribers.get(event, list())
        for subscription in subscriptions:
            subscription.func(event_object, **subscription.args)

        # Return the created object
        return event_object
