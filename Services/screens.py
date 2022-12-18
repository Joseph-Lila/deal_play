from kivy.uix.screenmanager import ScreenManager

from Controllers.schedule_configuration import ScheduleConfigurationController
from Models.schedule_configuration import ScheduleConfigurationModel

SCREENS = {
    "schedule configuration": {
        "model": ScheduleConfigurationModel,
        "controller": ScheduleConfigurationController
    }
}


class ScreenGenerator:
    """
    Generates views using models & controllers.
    Main method `generate_main_view` is used to get screen manager with all the views.
    """

    def __init__(self, screens=SCREENS):
        self.screens = screens

    def generate_main_view(self):
        """
        Method to get main view.
        :return:
        """
        sm = ScreenManager()
        for screen in self.screens:
            sm.add_widget(self._generate_view(screen))
        return sm

    def _generate_view(self, key):
        """
        Method to generate any view using key from `screens` field.
        :param key: str
        :return: view
        """
        model = self.screens[key]['model']()
        controller = self.screens[key]['controller'](model)
        view = controller.get_screen()
        view.name = key
        return view
