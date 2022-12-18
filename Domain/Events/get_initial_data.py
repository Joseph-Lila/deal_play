from dataclasses import dataclass

from Domain.Events.event import Event


@dataclass
class GetInitialDataEvent(Event):
    """
    Event to get days titles.
    """
    days: tuple
    groups: tuple
    mentors: tuple
    subjects: tuple
