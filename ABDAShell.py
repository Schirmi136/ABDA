import cmd
import networkx as nx
import matplotlib.pyplot as plt
from GraphVisualization.GraphConvert import GraphConvert
from GroundedDiscussionGame.Game import Game
from GroundedDiscussionGame.GameShell import GameShell


class ABDAShell(cmd.Cmd):
    intro = 'Welcome to ABDA. Type help or ? to list commands.\n'
    prompt = '> '

    def __init__(self, graph, grounded_extension, min_max):
        super().__init__()
        self.Graph = graph
        self.GroundedExtension = grounded_extension
        self.MinMax = min_max

    def do_print(self, arg):
        """print
        Prints the created argumentation graph"""
        G = GraphConvert.convert_to_networkx_graph(self.Graph, self.GroundedExtension, self.MinMax)
        pos = nx.planar_layout(G)

        fig, ax = plt.subplots()
        color_map = []
        for node in G.nodes:
            x, y = pos[node]
            if self.GroundedExtension[node] == 'in':
                color = "green"
            elif self.GroundedExtension[node] == 'out':
                color = "red"
            else:
                color = "yellow"
            ax.text(x, y, str(node), bbox=dict(facecolor=color, alpha=0.5), horizontalalignment='center')
            color_map.append(color)

        nx.draw(G, pos=pos, arrows=True, node_color="none", node_shape='s', arrowstyle='->')

        plt.show()

    def do_export_graph(self, arg):
        """export_graph
        Exports the graph as .graphml file."""
        G = GraphConvert.convert_to_networkx_graph(self.Graph, self.GroundedExtension, self.MinMax)
        nx.write_graphml(G, 'graphexport.graphml')

    def do_argument(self, arg):
        """argument [A]
        Prints the argument A with Conc(A),Sub(A), DefRules(A), LastDefRules(A), TopRule(A) """
        a = next((x for x in self.Graph.Arguments if str(x) == arg), None)
        if not a:
            print(arg + " is not a valid argument")
        else:
            a.dump()
            print("Min-Max: " + str(self.MinMax[a]))

    def do_arguments(self, arg):
        """arguments
        Prints the constructed arguments"""
        for a in self.Graph.Arguments:
            print(a)

    def do_all_warranted(self, arg):
        """warranted
        Prints all warranted arguments"""
        warranted_conclusions = set()
        for a in self.Graph.Arguments:
            if self.is_warranted(a.Conclusion):
                warranted_conclusions.add(a.Conclusion)
        for conclusion in warranted_conclusions:
            print(conclusion + " is warranted")

    def do_warranted(self, arg):
        """warranted [statement]
        Indicates whether [statement] can be justified"""
        if self.is_warranted(arg):
            print(arg + " is warranted")
        else:
            print(arg + " is not warranted")

    def do_discuss(self, arg):
        """discuss [statement]
        Discusses [statement] via the grounded discussion game. If [statement] is justified, the system will
        assume the role of the proponent and the user the role of the opponent, else vice versa."""
        ai_player = "P" if self.is_warranted(arg) else "O"
        arg_by_conclusion = next(filter(lambda k: k.Conclusion == arg, self.GroundedExtension.keys()), None)
        if arg_by_conclusion is None:
            print(arg + " is not a valid statement")
            return
        game = Game(self.Graph, arg_by_conclusion, self.GroundedExtension, self.MinMax)
        game_shell = GameShell(game, self.GroundedExtension, ai_player, arg_by_conclusion)
        game_shell.cmdloop()

    # noinspection PyMethodMayBeStatic
    def do_quit(self, arg):
        """Quits ABDA"""
        print("Bye!")
        return True

    def is_warranted(self, arg):
        return any(filter(lambda k: k.Conclusion == arg and self.GroundedExtension[k] == "in",
                          self.GroundedExtension.keys()))
