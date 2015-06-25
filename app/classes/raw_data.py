__author__ = 'Tadej'
import xlrd
class raw_data(object):
    accepted=None
    assigments=None
    def __init__(self, accepted_path, assigments_path):
        self.accepted = xlrd.open_workbook(accepted_path)
        self.assigments = open(assigments_path, 'r')