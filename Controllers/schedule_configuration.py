from Domain.Commands.command import Command
from Views.schedule_configuration.schedule_configuration import ScheduleConfigurationView


class ScheduleConfigurationController:
    """
    The `ScheduleConfigurationController` class represents a presenter implementation.
    Coordinates work of the view with the model.

    The presenter implements the strategy pattern. The controller connects to
    the view to control its actions.
    """

    def __init__(self, model):
        self.model = model
        self.view = ScheduleConfigurationView(controller=self, model=self.model)

    def get_screen(self):
        """ The method creates get the view. """

        return self.view

    def post_command_to_model(self, cmd: Command):
        self.model.handle(cmd)
