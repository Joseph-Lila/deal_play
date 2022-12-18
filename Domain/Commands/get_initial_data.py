from dataclasses import dataclass

from Domain.Commands.command import Command


@dataclass
class GetInitialDataCommand(Command):
    """
    Command to get days titles.
    """
