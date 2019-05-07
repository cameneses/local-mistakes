import networkx as nx
from importer import load_exclussions, load_log
import operator
import sys

# Not allowed sequences


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# Contains the model defined as a graph
class Model:

    # Creates a empty graph for the model
    def __init__(self):
        self.graph = nx.DiGraph()
   
    def add_nodes(self, nodes):
        for n in nodes:
            self.graph.add_node(n)

    def add_edge(self, start, end):
        self.graph.add_edge(start, end)

    # Check if the sequence of activities is allowed in the graph
    def check_allowed(self, start, end):
        if self.graph.has_edge(start, end):
            return True
        return False

    # Load model into a graph
    def load_graph(self, filename):
        with open(filename, "r") as file:
            for line in file:
                start, end = line.strip().split(";")
                self.add_edge(start, end)

    # Get the correct succ and pred for a sequence if it's a mistake
    def correct_activities(self, start=None, end=None):
        if start:
            succ = self.graph.successors(start)
            print("Correct successors for start activiy")
            for act in succ:
                print("\t{} -> ".format(start) + bcolors.BOLD +
                      "{}".format(act) + bcolors.ENDC)
        if end:
            pred = self.graph.predecessors(end)
            print("Correct predecessors for end activiy")
            for act in pred:
                print("\t" + bcolors.BOLD + "{}".format(act).format(act) +
                      bcolors.ENDC + " -> {}".format(end))

    
    def check_log(self, log):
        error_count = {}
        # Check mistakes and show correct successor and predecessor activities
        for k in cases.keys():
            print(k)
            case_errors = model.check_trace(cases[k])
            print("\n")
            for error in case_errors:
                seq = "{} -> {}".format(error[0], error[1])
                if seq not in error_count.keys():
                    error_count[seq] = 1
                else:
                    error_count[seq] += 1

        print("Mistakes summary")
        # Show mistakes ordered by frequency
        for k in sorted(error_count.items(), key=operator.itemgetter(1), reverse=True):
            edge = [a.strip() for a in k[0].strip().split("->")]
            print("\n{}\nCount: {}".format(k[0], k[1]))
            missing_activities = self.missing_activities(edge[0], edge[1])
            if len(missing_activities) > 0:
                seq = bcolors.BOLD + " -> ".join(missing_activities) + bcolors.ENDC
                print("Missing activities for this mistake")
                print("{} -> {} -> {}".format(edge[0], seq, edge[1]))
            else:
                print("This mistake doesn\'t have missing activities")
            
           

    def check_trace(self, trace):
        errors = []
        for i in range(len(trace) - 1):
            result = self.check_allowed(trace[i], trace[i+1])
            if not result:
                errors.append([trace[i], trace[i+1]])
                print("\n{} -> {}: {}".format(trace[i], trace[i+1], result))
                self.correct_activities(start=trace[i])
                self.correct_activities(end=trace[i+1])
        return errors

    def missing_activities(self, start, end):
        try:
            activities = nx.dijkstra_path(
                model.graph, start, end)[1:-1]
            return activities
        except nx.exception.NetworkXNoPath:
            return []


if len(sys.argv) < 3:
    print("Submit a exclussion file and a graph edges file")
    print("Example:\n python local_mistakes not_relevant.txt graph.csv")
else:
    not_relevant = load_exclussions(sys.argv[1])
    cases = load_log("CCC19 - Log CSV.csv", not_relevant)
    model = Model()
    model.load_graph(sys.argv[2])

    model.check_log(cases)



