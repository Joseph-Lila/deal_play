from dataclasses import dataclass

from Domain.Commands.command import Command


@dataclass
class GetConfigurationTableCommand(Command):
    day_of_week: str
    mod: str
    group: str
