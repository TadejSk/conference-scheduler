__author__ = 'Tadej'
from ..models import Paper
from sklearn import cluster
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.cluster import KMeans
class Clusterer:
    """
    TODO - Take into account graph data
         - Take into account locked and unlocked papers
         - Add an option to lock entire slots?
    :type papers: list[Paper]
    :type data_list : list[list[string]]
    """
    papers = []
    data = []
    cluster_distances = []
    cluster_values = []
    schedule = []
    schedule_settings = []
    num_clusters = 0
    slot_lengths = []
    slot_coords = []
    current_cluster = 1
    def __init__(self, papers: list, schedule: list, schedule_settings: list):
        self.papers = []
        self.data = []
        self.cluster_distances = []
        self.schedule = []
        self.schedule_settings = []
        self.num_clusters = 0
        self.slot_lengths = []
        self.slot_coords = []
        self.current_cluster = 1
        self.add_papers(papers)
        print("START PAPERS", len(self.papers))
        self.schedule = schedule
        self.schedule_settings = schedule_settings
        self.get_clusters()
        #self.find_papers_with_sum(self.papers,[],180,0,result)
        print("CLUSTERS:", self.slot_lengths)
        pass


    def add_papers(self, papers: list):
        for paper in papers:
            self.papers.append(paper)

    def add_slot_times(self, schedule_settings: list):
        self.schedule_settings = schedule_settings

    def get_clusters(self):
        """
        Calculates the clusters that will be needed based on the schedule structure and saves it into
        self.clusters. Also saves the amount of clusters into self.num_clusters
        :return: None
        """
        # Each unfilled schedule slot (a slot with no assigned papers) requires its own cluster
        self.num_clusters = 0
        for d,day in enumerate(self.schedule):
            for r,row in enumerate(day):
                for c,col in enumerate(row):
                    if col == []:
                        self.num_clusters += 1
                        self.slot_lengths.append(self.schedule_settings[d][r][c])
                        self.slot_coords.append([d,r,c])
        print(self.slot_lengths)

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
        clusterer = KMeans(n_clusters=self.num_clusters)
        self.cluster_distances = clusterer.fit_transform(self.data)
        self.cluster_values = clusterer.fit_predict(self.data).tolist()
        #for i in range(0,len(self.cluster_distances)):
        #    print(self.papers[i].title, "-", self.cluster_distances[i], aaa[i])

    def find_papers_with_sum(self, set, subset, desired_sum, curr_index, result):
        lens = [p.length for p in subset]
        if sum(lens) == desired_sum:
            indexes = []
            for paper in subset:
                indexes.append(self.papers.index(paper))
            result.append(indexes)
            return
        if sum(lens) > desired_sum:
            return
        for i in range(curr_index, len(set)):
            self.find_papers_with_sum(set, subset + [set[i]], desired_sum, i+1, result)



    def fit_to_schedule(self):
        """
        Assigns papers to clusters based on the self.cluster_distances obtained from the basic_clustering function
        Uses an iterative approach, where the biggest empty slot on the schedule is filled first, followed by the next
        biggest one, and so on until is no more papers that fit in the remaing empty time

        Possible imporovements:
            Should clustering be rerun after every slot is filled?
            Is there a better clustering algorithm?
            Is this iterative aproach even a good idea?
        """
        # Every paper should first have it's cluster and add_to_X fields reset
        for paper in self.papers:
            paper.add_to_day = -1
            paper.add_to_row = -1
            paper.add_to_col = -1
            paper.cluster = 0
            paper.save()
        # The following is repeated for every cluster independently
        while self.slot_lengths != []:
            # Get biggest empty slot
            slot_length = 0
            slot_index = 0
            for index,length in enumerate(self.slot_lengths):
                if length > slot_length:
                    slot_length = length
                    slot_index = index
            # Select biggest cluster
            cluster_sizes = [self.cluster_values.count(i) for i in range(0, self.num_clusters)]
            max_cluster = cluster_sizes.index(max(cluster_sizes))
            # Get papers from that cluster
            print(len(self.papers))
            print(len(self.cluster_values))
            cluster_papers = [p for p in self.papers if self.cluster_values[self.papers.index(p)] == max_cluster]
            # Select papers that fit into the slot
            papers = []
            self.find_papers_with_sum(cluster_papers, [], slot_length, 0, papers)
            if papers == []:
                print("NO SUITABLE COMBINATION FOUND")
            else:
                # if there are multiple fitting groups in the same cluster, select the group with the smallest error
                selected_index = 0
                if len(papers) > 1:
                    min_error = 9999999999999
                    for index,subset in enumerate(papers):
                        error = 0
                        for paper in subset:
                            error += self.cluster_distances[paper][max_cluster]*self.cluster_distances[paper][max_cluster]
                        print("ERROR: " + str(error))
                        if error < min_error:
                            selected_index = index
                            min_error = error
                    print(selected_index, min_error)
            # Update the papers' add_to_day/row/col fields. This fields will then be used to add the papers into the schedule
            # Also update the papers' cluster field
            ids = [self.papers[i].id for i in papers[selected_index]]
            papers_to_update = [self.papers[i] for i in papers[selected_index]]
            for paper in papers_to_update:
                paper.cluster = self.current_cluster
                coords = self.slot_coords[slot_index]
                paper.add_to_day = coords[0]
                paper.add_to_row = coords[1]
                paper.add_to_col = coords[2]
                paper.save()
            self.current_cluster += 1
            # remove the assigned papers from this class, since they no longer need to be assigned
            for paper in papers_to_update:
                self.papers.remove(paper)
            # also remove the information about the slot
            del self.slot_lengths[slot_index]
            del self.slot_coords[slot_index]
            print("END PAPERS", len(self.papers))

        """
        for max_time in self.slot_lengths:
            m = [[-1] * (max_time+1)] * self.num_clusters
            for i in range(0, max_time+1):
                m[0][i] = 0
            for i in range(0, self.num_clusters):
                for w in range(0, max_time+1):
                    if self.papers[i].length > w:
                        m[i][w] = m[i-1][w]
                    else:
                        m[i][w] = max(m[i-1][w], m[i-1][w-self.papers[i].length] + self.cluster_distances[i][0])
            print("MAX:", m[self.num_clusters-1][max_time])
        """