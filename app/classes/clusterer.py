import ast

__author__ = 'Tadej'
from ..models import Paper
from sklearn import cluster
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.cluster import KMeans, AffinityPropagation, DBSCAN, AgglomerativeClustering, MeanShift, MiniBatchKMeans
from sklearn.decomposition import PCA
import scipy.sparse
import numpy as np

class PaperGraph(object):

        class Connection(object):
            paper1 = None
            paper2 = None
            weight = 0
            def __init__(self, paper1, paper2, weight):
                self.paper1 = paper1
                self.paper2 = paper2
                self.weight = weight
            def __repr__(self):
                return "[" + str(self.paper1) + ", " + str(self.paper2) + ", " + str(self.weight) + "]"

        connections = []
        total_weights = {}
        nodes = []
        prob_matrix = []
        damping_factor = 0.85
        num_iterations = 20
        def __init__(self):
            #self.nodes = papers
            self.nodes = []
            self.connections = []

        def add_node(self, paper):
            self.nodes.append(paper)
            self.total_weights[paper] = 0

        def add_connection(self, paper1, paper2, weight):
            """
            Adds a new connection. If a connection already exists, then the weight is added to the existing connection's
            weight. If the weight is 0, the connection will not be created
            """
            if weight == 0:
                return
            for con in self.connections:
                if (con.paper1 == paper1 and con.paper2 == paper2) or (con.paper1 == paper2 and con.paper2 == paper1):
                    con.weight += weight
                    self.total_weights[paper1] += weight
                    self.total_weights[paper2] += weight
                    return
            connection = self.Connection(paper1, paper2, weight)
            self.total_weights[paper1] += weight
            self.total_weights[paper2] += weight
            self.connections.append(connection)

        def connection_weight(self, paper1, paper2):
            """
            returns the weight of the connection, or 0 if the nodes are not connected
            :return: int
            """
            for con in self.connections:
                if (con.paper1 == paper1 and con.paper2 == paper2) or (con.paper1 == paper2 and con.paper2 == paper1):
                    return con.weight
            return 0

        def create_probability_matrix(self):
            """
            In an unweighted graph, this is simply: M[i][j] = 1/OutboundConnections(j) if j links to i, or 0 otherwise
            In a weighted graph, it is therefore a*(1/OutCon(j)), where a is the weight of the connection from i to j
            Since the weight is the probability, it should be Weightij/Sum(weights of a node)
            :return:
            """
            self.prob_matrix = []
            for nodei in self.nodes:
                probs = []
                for nodej in self.nodes:
                    if nodei == nodej:
                        probs.append(0)
                    else:
                        if self.total_weights[nodei] == 0:
                            probs.append(0)     # Unconnected nodes would otherwise result in division by 0
                        else:
                            probs.append(self.connection_weight(nodei, nodej)/self.total_weights[nodei])
                self.prob_matrix.append(probs)
            #print("MATRIX: ")
            #print(self.prob_matrix)
            self.prob_matrix = np.array(self.prob_matrix)
            """
            for i in self.nodes:
                print(i, self.total_weights[i])
            for i in self.prob_matrix:
                print(sum(i))
            """
        def get_pr(self, start):
            """
            The pagerank of all papers will be stored in a vector PR[]
                PR[i] = pagerank of i
            Initial PR[i] is defined as 1/N, where N is the number of nodes in a graph (in this case the number of papers)
            The matrix M is the adjencency matrix, and Mij is defined as probability of reaching i from j
            E is a vector of zeroes, except for the value matching the starting node, where it is one
            We can then calculate PR as:
                PR' = (1-d)*E + d*M*PR
            """
            # Probability matrix is stored in self.prob_matrix
            # Isolated nodes (nodes with no connections) need to be treated seperately, since by normal calculation
            #   their pagerank does not sum to 1
            PR = []
            E = []
            row = 0
            for index, node in enumerate(self.nodes):
                if node == start:
                    E.append(1)
                    PR.append(1)
                    row = index
                else:
                    E.append(0)
                    PR.append(0)
            if sum(self.prob_matrix.tolist()[row]) < 0.1:
                return np.array(PR)
            #for none in self.nodes:
            #    PR.append(1/len(self.nodes))
            PR = np.array(PR)
            E = np.array(E)
            for iteration in range(1,self.num_iterations):
                PR = E*(1-self.damping_factor) + ((self.damping_factor) * np.transpose(self.prob_matrix).dot(PR))
            return PR


class ClusterPaper:
    cluster_distances = []
    coord_x = 0
    coord_y = 0
    cluster = 0
    paper = None
    assigned = False
    def __init__(self, paper):
        self.paper = paper

class ClusterSlot:
    is_parallel = False
    length = 0
    coords = []
    sub_slots = []
    def __init__(self):
        self.is_parallel = False
        self.length = 0
        self.coords = []
        self.sub_slots = []

    def add_sub_slot(self, slot):
        self.sub_slots.append(slot)

class Clusterer:
    """
    TODO - Take into account graph data
         - Take into account locked and unlocked papers
         - Add an option to lock entire slots?
    :type papers: list[ClusterPaper]
    :type data_list : list[list[string]]
    :type slots: list[ClusterSlot]
    """
    paper_graph = []
    papers = []
    data = []
    schedule = []
    schedule_settings = []
    slots = []
    current_cluster = 1
    cluster_function = None
    first_clustering = True
    num_clusters = 6
    graph_dataset = None
    using_graph_data = False
    using_abstracts = False
    using_titles = False
    cluster_function = ""
    vocab = []
    def __init__(self, papers: list, schedule: list, schedule_settings: list, func):
        self.vocab = []
        self.cluster_function = func
        self.papers = []
        self.data = []
        self.schedule = []
        self.schedule_settings = []
        self.current_cluster = 1
        self.num_clusters = 12
        self.graph_dataset = None
        self.add_papers(papers)
        self.reset_papers()
        self.schedule = schedule
        self.schedule_settings = schedule_settings
        self.first_clustering = True
        self.get_slots()
        # Needed, since clustering cannot be performed if n_samples < n_clusters

    def set_custom_vocabulary(self, vocab_string):
        words = vocab_string.split(' ')
        for word in words:
            self.vocab.append(word)

    def set_cluster_function(self, func):
        if len(self.papers) < self.num_clusters:
            self.num_clusters = len(self.papers)
        if func == 'aff':
            self.cluster_function = AffinityPropagation()
        if func =='dbs':
            self.cluster_function = DBSCAN()
        if func == 'hie':
            self.cluster_function = AgglomerativeClustering()
        if func == 'kme':
            self.cluster_function = KMeans(n_clusters=self.num_clusters)
        if func == 'msh':
            self.cluster_function = MeanShift()
        if func == 'kmm':
            self.cluster_function = MiniBatchKMeans(n_clusters=self.num_clusters)

    def add_papers(self, papers: list):
        for paper in papers:
            paper_to_add = ClusterPaper(paper)
            self.papers.append(paper_to_add)

    def add_slot_times(self, schedule_settings: list):
        self.schedule_settings = schedule_settings

    def add_graph(self, con_str):
        """
        Constructs a graph based on the papers currently in the class, and a string describing connections in the graph.
        The graph is stored in self.paper_graph.
        On top of that, a dataset created from the graph is stored in self.graph_dataset
        :param con_str: string
        :return: None
        """
        con_list = ast.literal_eval(con_str)
        self.paper_graph = PaperGraph()
        # First, add paper ids as nodes
        for paper in self.papers:
            self.paper_graph.add_node(paper.paper.id)
        # Then add connections
        for con in con_list:
            id1 = con[0]
            id2 = con[1]
            weight = con[2]
            # id1 and id2 are submission ids of a paper and need to be converted into regular ids
            found1 = False
            found2 = False
            for paper in self.papers:
                if paper.paper.submission_id == id1:
                    id1 = paper.paper.id
                    found1 = True
                    break
            for paper in self.papers:
                if paper.paper.submission_id == id2:
                    id2 = paper.paper.id
                    found2 = True
                    break
            # Then we can add the connection
            if found1 == True and found2 == True:
                self.paper_graph.add_connection(id1, id2, weight)
        # Create a probability matrix
        #
        self.paper_graph.create_probability_matrix()
        """
        print(self.paper_graph.prob_matrix[0])
        print(self.paper_graph.nodes[0])
        print("sums")
        """
        graph_dataset = []
        for node in self.paper_graph.nodes:
            pr = self.paper_graph.get_pr(node)
            graph_dataset.append(pr.tolist())
        self.graph_dataset = graph_dataset

    def get_slots(self):
        """
        Calculates the slots that will have to be filled based on the schedule structure and saves their lengths it into
        self.slot_lengths. Also saves the amount of slots into self.num_slot. Also saves the type of slot into
        self.parallel_slots
        :return: None
        """
        # Each unfilled schedule slot (a slot with no assigned papers) requires its own cluster
        for d,day in enumerate(self.schedule):
            for r,row in enumerate(day):
                if(len(row) > 1):
                    is_parallel = True
                    parent_slot = ClusterSlot()
                    for c, col in enumerate(row):
                        if col == []:
                            sub_slot = ClusterSlot()
                            sub_slot.length = self.schedule_settings[d][r][c]
                            sub_slot.coords = [d,r,c]
                            sub_slot.is_parallel = is_parallel
                            parent_slot.is_parallel = True
                            parent_slot.sub_slots.append(sub_slot)
                            # The parent slot length can be defined as the sum of all subslot lengths
                            parent_slot.length += sub_slot.length
                    self.slots.append(parent_slot)

                else:
                    is_parallel = False
                    for c,col in enumerate(row):
                        if col == []:
                            slot_to_add = ClusterSlot()
                            slot_to_add.length = self.schedule_settings[d][r][c]
                            slot_to_add.coords = [d,r,c]
                            slot_to_add.is_parallel = is_parallel
                            self.slots.append(slot_to_add)

    def simple_get_slots(self):
        for d,day in enumerate(self.schedule):
            for r,row in enumerate(day):
                if(len(row) > 1):
                    is_parallel = True
                else:
                    is_parallel = False
                for c,col in enumerate(row):
                    if col == []:
                        slot_to_add = ClusterSlot()
                        slot_to_add.length = self.schedule_settings[d][r][c]
                        slot_to_add.coords = [d,r,c]
                        slot_to_add.is_parallel = is_parallel
                        self.slots.append(slot_to_add)

    def create_dataset(self):
        self.data_list = []
        abstracts = []
        titles = []
        if self.vocab == []:
            count_vectorizer = CountVectorizer()
        else:
            count_vectorizer = CountVectorizer(vocabulary=self.vocab)
        tfid_transformer = TfidfTransformer()
        abstract_data = None
        title_data = None
        graph_data = None
        for paper in self.papers:
            abstracts.append(paper.paper.abstract)
            titles.append(paper.paper.title)
        if self.using_abstracts == True:
            print("using abstract data")
            abstract_count = count_vectorizer.fit_transform(abstracts)
            abstract_tfid = tfid_transformer.fit_transform(abstract_count)
            abstract_data = abstract_tfid
        if self.using_titles == True:
            print("using title data")
            title_count = count_vectorizer.fit_transform(titles)
            abstract_tfid = tfid_transformer.fit_transform(title_count)
            title_data = abstract_tfid
        if self.using_graph_data == True:
            print("using graph data")
            graph_data = scipy.sparse.csr_matrix(np.matrix(self.graph_dataset))
        self.data = []
        for paper in self.papers:
            self.data.append([0])
        self.data=scipy.sparse.csr_matrix(self.data)
        if abstract_data != None:
            self.data = scipy.sparse.hstack([self.data, abstract_data])
        if title_data != None:
            self.data = scipy.sparse.hstack([self.data, title_data])
        if graph_data != None:
            self.data = scipy.sparse.hstack([self.data, graph_data])
        print("DATA")
        print(self.data.toarray()[0])

    def basic_clustering(self):
        cluster_values = self.cluster_function.fit_predict(self.data).tolist()
        if self.cluster_function == 'kmm' or self.cluster_function == 'kme':
            cluster_distances = self.cluster_function.fit_transform(self.data)
        else:
            cluster_distances = []
            for paper in self.papers:
                d = []
                for a in range(0,len(cluster_values)):
                    d.append(0)
                cluster_distances.append(d)
        for index,distance in enumerate(cluster_distances):
            self.papers[index].cluster_distances = distance
        for index,value in enumerate(cluster_values):
            self.papers[index].cluster = value
        # Assign basic clusters to papers
        if self.first_clustering == True:
            print("first clustering")
            for paper in self.papers:
                print("assigned ", paper.cluster, "to paper " ,paper.paper.title)
                paper.paper.simple_cluster = paper.cluster
        # Get coordinates for visualization
        self.get_coords()
        #for i in range(0,len(self.cluster_distances)):
        #    print(self.papers[i].title, "-", self.cluster_distances[i])

    def find_papers_with_sum(self, set, subset, desired_sum, curr_index, result):
        lens = [p.paper.length for p in subset]
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

    def get_coords(self):
        if(len(self.papers) == 1):
            visual_coords_x = [0]
            visual_coords_y =  [0]
        else:
            self.create_dataset()
            if scipy.sparse.issparse(self.data):
                data = self.data.toarray()
            else:
                data = self.data
            pca_data = PCA(n_components=2).fit_transform(data)
            self.cluster_function.fit(pca_data)
            #print("--------------COORDS------------")
            #print(pca_data[:,0])
            #print(pca_data[:,1])
            visual_coords_x = pca_data[:,0]
            visual_coords_y =  pca_data[:,1]
        for index, x in enumerate(visual_coords_x):
            self.papers[index].coord_x = x
        for index, y in enumerate(visual_coords_y):
            self.papers[index].coord_y = y
        if self.first_clustering == True:
            for paper in self.papers:
              #  paper.paper.simple_cluster = paper.paper.cluster
                paper.paper.simple_visual_x = paper.coord_x
                paper.paper.simple_visual_y = paper.coord_y
                paper.paper.save()
                self.first_clustering = False

    def reset_papers(self):
        for paper in self.papers:
            paper.paper.add_to_day = -1
            paper.paper.add_to_row = -1
            paper.paper.add_to_col = -1
            paper.paper.cluster = 0
            paper.paper.simple_cluster = 0
            paper.paper.save()

    def fit_to_schedule2(self):
        """
        An alternate approach approach:
            1.) Perform clustering with basic_clustering - done manually in the view
            2.) Select a cluster with papers most similar to one another and fill a slot
            3.) Fill slots in the following order: single slots, parallel slots
            4.) With parallel slots, each slot should be filled with papers from a different cluster - prefferebly the
                cluster centroids of such clusters should be as far away as possible
            5.) Repeat untill all slots are filled
        """
        # The following is repeated for every cluster independently
        # Slot lengths are initialized in __init__
        previous_clusters = []  # Used when picking clusters for parallel slots
        while self.slots != []:
            do_break = False
            # Get biggest empty slot - only select parallel slots once all non-parallel slots have already been filled
            slot_length = 0
            slot_index = 0
            sub_slot = None
            num_nonparallel = 0
            for slot in self.slots:
                if slot.is_parallel == False:
                    num_nonparallel += 1
            for index,slot in enumerate(self.slots):
                if slot.length > slot_length:
                    # Skip parallel slots until there are no other options
                    if num_nonparallel > 0 and slot.is_parallel == True:
                        continue
                    if slot.is_parallel:
                        # For parallel slots, pick the first unfilled subslot. If all subslots have been filled,
                        # delete the slot and continue
                        if len(slot.sub_slots) == 0:
                            previous_clusters = []
                            del self.slots[slot_index]
                            # If the deleted slot was the last one, the loop should end
                            if self.slots == []:
                                do_break = True;
                            continue
                        else:
                            sub_slot = slot.sub_slots[0]
                    slot_length = slot.length
                    slot_index = index
            # If slot is not parallel, select a single cluster
            if do_break:
                break
            if not self.slots[slot_index].is_parallel:
                # Select biggest cluster
                cluster_values = [paper.cluster for paper in self.papers]
                cluster_sizes = [cluster_values.count(i) for i in range(0, len(self.slots))]
                max_cluster = cluster_sizes.index(max(cluster_sizes))
                # Get papers from that cluster
                cluster_papers = [p for p in self.papers if p.cluster == max_cluster]
            else:
                # If the slot is parallel, then consider previous clusters
                cluster_values = [paper.cluster for paper in self.papers]
                cluster_sizes = [cluster_values.count(i) for i in range(0, len(self.slots))]
                max_size = 0
                for index,size in enumerate(cluster_sizes):
                    if index in previous_clusters:
                        continue
                    if size > max_size:
                        max_size = size
                        max_cluster = index
                cluster_papers = [p for p in self.papers if p.cluster == max_cluster]
            # If slot is parallel, then the previous clusters must also be considered - simultaneous parallel slots should
            # be filled whith papers from different clusters
            # Select papers that fit into the slot
            papers = []
            self.find_papers_with_sum(cluster_papers, [], slot_length, 0, papers)
            if papers == []:
                # This happens when there are no papers, that can completely fill a slot in the largest cluster.
                # In this case, it makes sense to rerun clustering with less clusters, as that should produce clusters
                #   with more papers.
                # If even that doesnt help, then the function should end end report this to the user
                if self.num_clusters == 1:
                    return False
                else:
                    # Needed, since clustering cannot be performed if n_samples < n_clusters
                    self.num_clusters -= 1
                    self.set_cluster_function(self.cluster_function)
                    self.create_dataset()
                    self.basic_clustering()
                    print("NO SUITABLE COMBINATION FOUND2")
                    return self.fit_to_schedule2()
            else:
                # if there are multiple fitting groups in the same cluster, select the group with the smallest error
                selected_index = 0
                if len(papers) > 1:
                    min_error = 9999999999999
                    for index,subset in enumerate(papers):
                        error = 0
                        for paper in subset:
                            error += self.papers[paper].cluster_distances[max_cluster]*self.papers[paper].cluster_distances[max_cluster]
                        if error < min_error:
                            selected_index = index
                            min_error = error
            # Update the papers' add_to_day/row/col fields. This fields will then be used to add the papers into the schedule
            # Also update the papers' cluster field
            ids = [self.papers[i].paper.id for i in papers[selected_index]]
            papers_to_update = [(self.papers[i],i) for i in papers[selected_index]]
            #print("PAPERS TO UPATE: ", papers_to_update)
            # Return the cluster coordinates - used for visualization
            for paper, index in papers_to_update:
                paper.paper.cluster = self.current_cluster
                if not self.slots[slot_index].is_parallel:
                    coords = self.slots[slot_index].coords
                else:
                    coords = sub_slot.coords
                paper.paper.add_to_day = coords[0]
                paper.paper.add_to_row = coords[1]
                paper.paper.add_to_col = coords[2]
                #print("COORD ",  index, self.visual_coords_x[index], self.visual_coords_y[index])
                paper.paper.visual_x = paper.coord_x
                paper.paper.visual_y = paper.coord_y
                paper.paper.save()
            self.current_cluster += 1
            # remove the assigned papers from this class, since they no longer need to be assigned
            offset = 0
            for paper, index in papers_to_update:
                self.papers.remove(paper)
                # Remove the relevant line from graph dataset
                if self.using_graph_data == True:
                    graph = len(self.graph_dataset)
                    del self.graph_dataset[index - offset]
                    # since indexes are sorted in asending order, they must be updated, which is handled by offset
                    offset += 1
            # also remove the information about the slot
            if not self.slots[slot_index].is_parallel:
                del self.slots[slot_index]
            else:
                del self.slots[slot_index].sub_slots[0]
            # redo clustering
            #self.set_cluster_function(self.cluster_function)
            #self.create_dataset()
            #self.basic_clustering()
