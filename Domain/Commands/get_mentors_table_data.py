from dataclasses import dataclass

from Domain.Commands.command import Command


@dataclass
class GetMentorsTableDataCommand(Command):
    mentor: str
