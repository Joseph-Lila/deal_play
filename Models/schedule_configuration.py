import datetime
from datetime import date
from functools import partial

from loguru import logger
from Domain.Commands.command import Command
from Domain.Commands.get_configuration_table import GetConfigurationTableCommand
from Domain.Commands.get_groups_table_data import GetGroupsTableDataCommand
from Domain.Commands.get_initial_data import GetInitialDataCommand
from Domain.Commands.get_mentors_table_data import GetMentorsTableDataCommand
from Domain.Commands.reset_configuration_table import ResetConfigurationTableCommand
from Domain.Events.event import Event
from Domain.Events.get_configuration_table import GetConfigurationTableEvent
from Domain.Events.get_groups_table_data import GetGroupsTableDataEvent
from Domain.Events.get_initial_data import GetInitialDataEvent
from Domain.Events.get_mentors_table_data import GetMentorsTableDataEvent
from Domain.Events.reset_configuration_table import ResetConfigurationTableEvent
from Services.observer import Observer


class ScheduleConfigurationModel(Observer):
    """ The ScheduleConfigurationModel class """

    def __init__(self):
        super().__init__()
        self.subjects = ('Матем.',)
        self.workload = [
            ['Мур Я.С.', 'Матем.', 'ИП-41', [0, 60], [0, 60]],
            ['Мур Я.С.', 'Матем.', 'ИП-42', [0, 60], [0, 60]],
        ]

        self.days_of_week = ('ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ')
        self.mods = ('Над чертой', 'Под чертой')
        self.groups = ('ИП-41', 'ИП-42')
        self.mentors = ('Мур Я.С.',)
        self.configuration_tables = {
            (day_of_week, mod, group): {i + 1: None for i in range(6)}
            for mod in self.mods
            for day_of_week in self.days_of_week
            for group in self.groups
        }

    def handle(self, cmd: Command, *args, **kwargs):
        logger.debug(f'handling command {cmd}')
        try:
            self.notify_observers(self.process_command(cmd))
        except Exception:
            logger.exception("Exception handling command %s", cmd)
            raise

    def process_command(self, cmd: Command):
        if type(cmd) == GetInitialDataCommand:
            return GetInitialDataEvent(
                days=self.days_of_week,
                groups=self.groups,
                mentors=self.mentors,
                subjects=self.subjects,
            )
        elif type(cmd) == GetConfigurationTableCommand:
            return GetConfigurationTableEvent(
                day_of_week=cmd.day_of_week,
                mod=cmd.mod,
                group=cmd.group,
                configuration_table=self.configuration_tables[(cmd.day_of_week, cmd.mod, cmd.group)]
            )
        elif type(cmd) == ResetConfigurationTableCommand:
            self._clear_configuration()
            self._reset_mentors_workload()
            return ResetConfigurationTableEvent()
        elif type(cmd) == GetMentorsTableDataCommand:
            return GetMentorsTableDataEvent(
                mentor=cmd.mentor,
                mentors_workload=self._get_mentors_workload(cmd.mentor),
                mentors_quantity=len(self.mentors),
                current_quantity=self._get_mentors_quantity_with_complete_hours()
            )
        elif type(cmd) == GetGroupsTableDataCommand:
            return GetGroupsTableDataEvent(
                group=cmd.group,
                current_groups=self._get_groups_quantity_with_complete_hours(),
                groups_quantity=len(self.groups),
                groups_workload=self._get_groups_workload(cmd.group)
            )

    def _get_mentors_workload(self, mentor):
        workload = []
        for item in self.workload:
            if item[0] == mentor:
                workload.append([item[1], item[2], item[3], item[4]])
        return workload

    def _get_groups_workload(self, group):
        workload = []
        for item in self.workload:
            if item[2] == group:
                workload.append([item[1], item[0], item[3], item[4]])
        return workload

    def _get_groups_quantity_with_complete_hours(self):
        ans = 0
        for group in self.groups:
            done = True
            for record in self.workload:
                if record[2] != group:
                    continue
                if record[3][0] != record[3][1] or record[4][0] != record[4][1]:
                    done = False
                    break
            if done:
                ans += 1
        return ans

    def _get_mentors_quantity_with_complete_hours(self):
        ans = 0
        for mentor in self.mentors:
            done = True
            for record in self.workload:
                if record[0] != mentor:
                    continue
                if record[3][0] != record[3][1] or record[4][0] != record[4][1]:
                    done = False
                    break
            if done:
                ans += 1
        return ans

    def _clear_configuration(self):
        for config_table in self.configuration_tables:
            for key in self.configuration_tables[config_table]:
                self.configuration_tables[config_table][key] = None

    def _reset_mentors_workload(self):
        for record in self.workload:
            record[3][0] = 0
            record[4][0] = 0
