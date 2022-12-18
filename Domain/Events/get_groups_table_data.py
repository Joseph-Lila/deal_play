from dataclasses import dataclass

from Domain.Events.event import Event


@dataclass
class GetGroupsTableDataEvent(Event):
    group: str
    groups_workload: list
    groups_quantity: int
    current_groups: int
