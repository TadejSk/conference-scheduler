__author__ = 'Tadej'
import ast

"""
The class is used to serialize and deserialize schedule information between a python list and a settings string
The settings are stored in the following format
settings_list: [[dayx_list]*]
dayx_list:[slot*]
slot:sequential_slots* | [parallel_slots*]
sequential_slot: [paper_id*],
parallel_slot: [paper_id*],
paper_id: int
Example:
    The list [[[1], [2], [3,8] [[4], [5,6], [7]] would create the folowing timetable

                    SLOT1: paper1
                    SLOT2: paper2
                    SLOT3: paper3 and paper8
    SLOT4:paper 4   SLOT4: paper5 and paper6   SLOT4:paper7

    Where each slot is 60 minutes long and occurs on day 1
"""

class schedule_manager_class(object):
    papers=[]
    def __init__(self):
        return

    """
    def __init__(self, paper_string, num_days:int):
        if paper_string == "":
            self.papers = []
            for i in range(num_days):
                self.papers.append([])
        else:
            self.papers = ast.literal_eval(paper_string)
        return
    """
    def create_empty_list(self, settings_string):
        list = []
        settings = ast.literal_eval(settings_string)
        print(settings)
        for day_string in settings:
            day_list = []
            for slots in day_string:
                if type(slots) == int:
                    print("aaa")
                    day_list.append([])
                else:
                    print("bbb")
                    slot_list = []
                    for slot in slots:
                        slot_list.append([])
                    day_list.append(slot_list)
            list.append(day_list)
        self.papers = list
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
        return

    def change_slot_time(self, day:int, row:int, col:int, new_len:int):
        day_schedule = self.settings[day]
        row_schedule = day_schedule[row]
        if type(row_schedule) == int:
            day_schedule[row] = new_len
        else:
            row_schedule[col] = new_len
        print(self.settings)
        return

    def __str__(self):
        return str(self.settings)

