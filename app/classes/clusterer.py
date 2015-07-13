__author__ = 'Tadej'
from ..models import Paper
from sklearn import cluster
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.cluster import KMeans
class Clusterer:
    """
    :type papers: list[Paper]
    :type data_list : list[list[string]]
    """
    papers = []
    data = []
    cluster_distances = []
    def __init__(self):
        pass

    def add_papers(self, papers: list):
        for paper in papers:
            self.papers.append(paper)

    def create_dataset(self):
        self.data_list = []
        abstracts = []
        for paper in self.papers:
            abstracts.append(paper.abstract)
        count_vectorizer = CountVectorizer()
        abstract_count = count_vectorizer.fit_transform(abstracts)
        tfid_transformer = TfidfTransformer()
        abstract_tfid = tfid_transformer.fit_transform(abstract_count)
        self.data = abstract_tfid


    def basic_clustering(self):
        clusterer = KMeans(n_clusters=4)
        self.cluster_distances = clusterer.fit_transform(self.data)
        for i in range(0,len(self.cluster_distances)):
            print(self.papers[i].title, "-", self.cluster_distances[i])

    def fit_to_schedule(self):
        pass