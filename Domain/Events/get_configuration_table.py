from dataclasses import dataclass

from Domain.Events.event import Event


@dataclass
class GetConfigurationTableEvent(Event):
    day_of_week: str
    mod: str
    group: str
    configuration_table: dict
