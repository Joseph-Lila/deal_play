from dataclasses import dataclass

from Domain.Events.event import Event


@dataclass
class GetMentorsTableDataEvent(Event):
    mentor: str
    mentors_workload: list
    mentors_quantity: int
    current_quantity: int
