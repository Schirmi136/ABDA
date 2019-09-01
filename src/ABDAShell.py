import cmd
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

    def do_warranted(self, arg):
        """warranted [statement]
        Indicated whether [statement] can be justified"""
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
        game_shell = GameShell(game, ai_player, arg_by_conclusion)
        game_shell.cmdloop()

    # noinspection PyMethodMayBeStatic
    def do_quit(self, arg):
        """Quits ABDA"""
        print("Bye!")
        return True

    def is_warranted(self, arg):
        return any(filter(lambda k: k.Conclusion == arg and self.GroundedExtension[k] == "in",
                          self.GroundedExtension.keys()))
