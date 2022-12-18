from dataclasses import dataclass

from Domain.Commands.command import Command


@dataclass
class ResetConfigurationTableCommand(Command):
    """
    Command to reset configuration table
    """
