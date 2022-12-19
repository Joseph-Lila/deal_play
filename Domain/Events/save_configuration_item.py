from dataclasses import dataclass

from Domain.Events.event import Event


@dataclass
class SaveConfigurationItemEvent(Event):
    configuration_table: dict
