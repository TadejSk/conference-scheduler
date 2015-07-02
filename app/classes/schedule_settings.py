__author__ = 'Tadej'
import ast

"""
The class is used to serialize and deserialize settings between a python list and a settings string
The settings are stored in the following format
settings_list: [[dayx_list]*]
dayx_list:[slot*]
slot:sequential_slot* | [parallel_slot*]
sequential_slot: time_in_minutes,
parallel_slot: time_in_minutes,
Example:
    The list [[60, 60, 60 [60, 60, 60], [60, 60, 60], 60]] would create the folowing timetable

            SLOT1
            SLOT2
            SLOT3
    SLOT4   SLOT4   SLOT4
    SLOT5   SLOT5   SLOT5
            SLOT6

    Where each slot is 60 minutes long and occurs on day 1
"""
class schedule_settings_class(object):
    settings=[]
    def __init__(self, settings_string, num_days:int):
        if settings_string == "":
            self.settings = []
            for i in range(num_days):
                self.settings.append([])
        else:
            self.settings = ast.literal_eval(settings_string)
            if len(self.settings) < num_days:
                for i in range(num_days-len(self.settings)):
                    self.settings.append([])
            if len(self.settings) > num_days:
                self.settings = self.settings[:num_days]
        return

    def add_slot_to_day(self, day:int, slot_length:int):
        day_schedule = self.settings[day]
        day_schedule.append(slot_length)
        return

    def add_parallel_slots_to_day(self, day:int, slot_length:int, num_slots:int):
        day_schedule = self.settings[day]
        parallel_slots = []
        for i in range(num_slots):
            parallel_slots.append(slot_length)
        day_schedule.append(parallel_slots)
    def __str__(self):
        return str(self.settings)

