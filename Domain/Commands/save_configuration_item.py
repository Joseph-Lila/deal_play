from dataclasses import dataclass

from Domain.Commands.command import Command


@dataclass
class SaveConfigurationItemCommand(Command):
    group: str
    day_of_week: str
    mod: str
    place: str
    mentor: str
    kind: str
    number_of_class: int
