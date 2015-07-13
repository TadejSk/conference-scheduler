__author__ = 'Tadej'
import xlrd
from ..models import Author, Paper
from .paper import paper
class raw_data(object):
    accepted=None
    assigments=None
    accepted_papers_list = []
    def __init__(self, accepted_path, assigments_path):
        self.accepted = xlrd.open_workbook(accepted_path)
        self.assigments = open(assigments_path, 'r')

    def parse_accepted(self):
        sheet = self.accepted.sheet_by_index(0)
        for row in range(1,sheet.nrows):
            id = sheet.cell_value(rowx = row, colx = 0)
            title = sheet.cell_value(rowx = row, colx = 2)
            abstract = sheet.cell_value(rowx = row, colx = 3)
            authors = []
            for author in str(sheet.cell_value(rowx = row, colx = 1)).replace(" and ",", ").replace(".","").split(", "):
                if(author.endswith(' ')):
                    author = author[:-1]
                authors.append(author)
            p = paper(authors=authors, abstract=abstract, title=title, submission_id = id)
            self.accepted_papers_list.append(p)
        return self