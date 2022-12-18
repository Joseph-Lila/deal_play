from kivy.factory import Factory
from kivy.metrics import dp
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import MDScreen

from Domain.Commands.get_configuration_table import GetConfigurationTableCommand
from Domain.Commands.get_groups_table_data import GetGroupsTableDataCommand
from Domain.Commands.get_initial_data import GetInitialDataCommand
from Domain.Commands.get_mentors_table_data import GetMentorsTableDataCommand
from Domain.Events.event import Event
from Domain.Events.get_configuration_table import GetConfigurationTableEvent
from Domain.Events.get_groups_table_data import GetGroupsTableDataEvent
from Domain.Events.get_initial_data import GetInitialDataEvent
from Domain.Events.get_mentors_table_data import GetMentorsTableDataEvent
from Domain.Events.reset_configuration_table import ResetConfigurationTableEvent
from Services.observable import Observable


class ScheduleConfigurationView(MDScreen, Observable):
    """
    A class that implements the visual representation `ScheduleConfigurationModel`
    """
    controller = ObjectProperty()
    model = ObjectProperty()

    def __init__(self, **kw):
        super().__init__(**kw)
        self.model.add_observer(self)
        self.table_ceil_list = [
            self.configuration.first, self.configuration.second, self.configuration.third,
            self.configuration.fourth, self.configuration.fifth, self.configuration.sixth
        ]
        self.controller.post_command_to_model(GetInitialDataCommand())
        self._init_menus()

    def _init_menus(self):
        self._init_days_of_week_menu()
        self._init_groups_menu()
        self._init_mentors_table_menu()

    def _init_days_of_week_menu(self):
        self.days_of_week_menu = MDDropdownMenu(
            caller=self.configuration.day_of_week_drop,
            items=self._get_days_of_week_menu_items(),
            width_mult=2,
            max_height=dp(200),
            position="bottom",
            radius=[24, 0, 24, 0],
        )

    def _init_groups_menu(self):
        self.groups_menu = MDDropdownMenu(
            caller=self.configuration.group_drop,
            items=self._get_groups_menu_items(),
            width_mult=3,
            max_height=dp(200),
            position="bottom",
            radius=[24, 0, 24, 0],
        )

    def _init_mentors_table_menu(self):
        self.mentors_table_menu = MDDropdownMenu(
            caller=self.mentors.drop,
            items=self._get_mentors_table_menu_items(),
            width_mult=4,
            max_height=dp(200),
            position="bottom",
            radius=[24, 0, 24, 0],
        )

    def _init_groups_table_menu(self):
        self.groups_table_menu = MDDropdownMenu(
            caller=self.groups.drop,
            items=self._get_groups_table_menu_items(),
            width_mult=4,
            max_height=dp(200),
            position="bottom",
            radius=[24, 0, 24, 0],
        )

    def _get_groups_table_menu_items(self):
        groups_table_menu_items = [
            {
                "text": group,
                "viewclass": "OneLineListItem",
                "on_release": lambda x=group: self.controller.post_command_to_model(
                    GetGroupsTableDataCommand(
                        mentor=x
                    )
                )
            } for group in self._groups
        ]
        return groups_table_menu_items

    def _get_mentors_table_menu_items(self):
        mentors_table_menu_items = [
            {
                "text": mentor,
                "viewclass": "OneLineListItem",
                "on_release": lambda x=mentor: self.controller.post_command_to_model(
                    GetMentorsTableDataCommand(
                        mentor=x
                    )
                )
            } for mentor in self._mentors
        ]
        return mentors_table_menu_items

    def _get_groups_menu_items(self):
        groups_menu_items = [
            {
                "text": group,
                "viewclass": "OneLineListItem",
                "on_release": lambda x=group: self.controller.post_command_to_model(
                    GetConfigurationTableCommand(
                        mod='Над чертой' if self.configuration.under_line_checkbox.active else 'Под чертой',
                        group=x,
                        day_of_week=self.configuration.day_of_week_drop.text
                    )
                )
            } for group in self._groups
        ]
        return groups_menu_items

    def _get_days_of_week_menu_items(self):
        days_of_week_menu_items = [
            {
                "text": day,
                "viewclass": "OneLineListItem",
                "on_release": lambda x=day: self.controller.post_command_to_model(
                    GetConfigurationTableCommand(
                        mod='Над чертой' if self.configuration.under_line_checkbox.active else 'Под чертой',
                        group=self.configuration.group_drop.text,
                        day_of_week=x
                    )
                )
            } for day in self._days_of_week
        ]
        return days_of_week_menu_items

    def model_is_changed(self, event: Event):
        if type(event) == GetInitialDataEvent:
            self.initialize_data(event)
        elif type(event) == GetConfigurationTableEvent:
            self.change_configuration_table(event)
        elif type(event) == ResetConfigurationTableEvent:
            self._make_config_item_free()
        elif type(event) == GetMentorsTableDataEvent:
            self._update_mentors_table(event)
        elif type(event) == GetGroupsTableDataEvent:
            self._update_groups_table(event)

    def initialize_data(self, event: Event):
        self._days_of_week = event.days
        self._mentors = event.mentors
        self._groups = event.groups
        self._subjects = event.subjects
        self._init_configuration_screen()

    def _init_configuration_screen(self):
        self.configuration.day_of_week_drop.text = self.configuration.day_of_week.text = self._days_of_week[0]
        self.configuration.group.text = self.configuration.group_drop.text = self._groups[0]
        self.controller.post_command_to_model(GetMentorsTableDataCommand(mentor=self._mentors[0]))
        self.controller.post_command_to_model(GetGroupsTableDataCommand(group=self._groups[0]))

    def change_configuration_table(self, event: Event):
        self._cur_configuration_table = event.configuration_table
        self.configuration.day_of_week_drop.text = self.configuration.day_of_week.text = event.day_of_week
        self.configuration.group.text = self.configuration.group_drop.text = event.group
        self.configuration.under_line_checkbox.active = True if event.mod == 'Над чертой' else False

    def _update_mentors_table(self, event: Event):
        self.mentors.drop.text = event.mentor
        color = 'ff0000' if event.mentors_quantity != event.current_quantity else '00ff00'
        self.mentors.title.text = f'ПРЕПОДАВАТЕЛИ: [color=#{color}]{event.current_quantity}/{event.mentors_quantity}[/color]'
        self.mentors.mentor_records.clear_widgets()

        for record in event.mentors_workload:
            subject_btn = self._get_table_button(record[0])
            group_btn = self._get_table_button(record[1])
            labs_btn = self._get_table_button(f'{record[2][0]}/{record[2][1]}',
                                              color='red' if record[2][0] != record[2][1] else 'green')
            practices_btn = self._get_table_button(f'{record[3][0]}/{record[3][1]}',
                                                   color='red' if record[3][0] != record[3][1] else 'green')
            self.mentors.mentor_records.add_widget(subject_btn)
            self.mentors.mentor_records.add_widget(group_btn)
            self.mentors.mentor_records.add_widget(labs_btn)
            self.mentors.mentor_records.add_widget(practices_btn)

    def _get_table_button(self, text, color='black'):
        btn = MDRaisedButton(
            text=text, halign='center', disabled=True, disabled_color=color,
            md_bg_color_disabled=(217 / 255, 217 / 255, 217 / 255, 1), size_hint=(.9, None),
        )
        return btn

    def _make_config_item_free(self):
        # update mentors table
        self.controller.post_command_to_model(GetMentorsTableDataCommand(mentor=self.mentors.drop.text))

        # free table
        for table_ceil in self.table_ceil_list:
            table_ceil.clear_widgets()

        # add empty elements
        for table_ceil in self.table_ceil_list:
            table_ceil.add_widget(Factory.ConfigurationTableItem(size_hint=(1, 1), text="+"))

        # bind new empty elements

    def _update_groups_table(self, event: Event):
        self.groups.drop.text = event.group
        color = 'ff0000' if event.groups_quantity != event.current_groups else '00ff00'
        self.groups.title.text = f'ГРУППЫ: [color=#{color}]{event.current_groups}/{event.groups_quantity}[/color]'
        self.groups.group_records.clear_widgets()

        for record in event.groups_workload:
            subject_btn = self._get_table_button(record[0])
            mentor_btn = self._get_table_button(record[1])
            labs_btn = self._get_table_button(f'{record[2][0]}/{record[2][1]}',
                                              color='red' if record[2][0] != record[2][1] else 'green')
            practices_btn = self._get_table_button(f'{record[3][0]}/{record[3][1]}',
                                                   color='red' if record[3][0] != record[3][1] else 'green')
            self.groups.group_records.add_widget(subject_btn)
            self.groups.group_records.add_widget(mentor_btn)
            self.groups.group_records.add_widget(labs_btn)
            self.groups.group_records.add_widget(practices_btn)
