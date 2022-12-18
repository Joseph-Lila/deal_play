from dataclasses import dataclass

from Domain.Events.event import Event


@dataclass
class ResetConfigurationTableEvent(Event):
    """
    Command to reset configuration table
    """
