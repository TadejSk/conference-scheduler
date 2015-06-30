__author__ = 'Tadej'
class paper(object):
    authors = []
    title = ""
    abstract = ""
    def __init__(self, title, authors, abstract):
        self.authors = authors
        self.title = title
        self.abstract = abstract