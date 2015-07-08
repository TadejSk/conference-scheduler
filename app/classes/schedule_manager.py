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
                    day_list.append([[]])
                else:
                    slot_list = []
                    for slot in slots:
                        slot_list.append([])
                    day_list.append(slot_list)
            list.append(day_list)
        self.papers = list
        return

    def import_paper_schedule(self, schedule_string:str):
        self.papers = ast.literal_eval(schedule_string)

    def assign_paper(self, paper:int, day:int, slot_row:int, slot_col:int):
        self.remove_paper(paper)
        print(day, slot_row, slot_col)
        day = self.papers[day]
        row = day[slot_row]
        col = row[slot_col]
        col.append(paper)
        return

    def remove_paper(self, paper:int):
        for di,day_list in enumerate(self.papers):
            print("day_list:" + str(day_list))
            for ri,row in enumerate(day_list):
                print("row:" + str(row))
                for ci,col in enumerate(row):
                    print("col:" + str(col))
                    for i in range(0,len(col)):
                        print(col[i],paper, col[i]==paper)
                        if col[i] == paper:
                            col = col[0:i] + col[i+1:len(col)]
                            print(col)
                            self.papers[di][ri][ci] = col
                            print(self.papers)
                            return True
        print("b")
        return False

    def __str__(self):
        return str(self.settings)

