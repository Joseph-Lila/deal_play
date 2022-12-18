from dataclasses import dataclass

from Domain.Commands.command import Command


@dataclass
class GetGroupsTableDataCommand(Command):
    group: str
