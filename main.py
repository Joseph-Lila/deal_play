from kivy.core.window import Window
from kivymd.app import MDApp

from Services.screens import ScreenGenerator

Window.size = (1137, 786)


class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.load_all_kv_files(self.directory)

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Indigo"
        self.theme_cls.primary_hue = "700"
        self.theme_cls.material_style = "M3"
        return ScreenGenerator().generate_main_view()


if __name__ == "__main__":
    MainApp().run()
