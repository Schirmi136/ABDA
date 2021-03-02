import networkx as nx
class GraphConvert:
    @staticmethod
    def ConvertToNetworkXGraph(graph):
        """
        Converts a given argumentations graph to a printable networkX graph
        """
        G = nx.Graph()
        for argument in graph.Arguments:
            G.add_node(str(argument))
        for attack in graph.Attacks:
            G.add_edge(str(attack.From), str(attack.To))
        return G
