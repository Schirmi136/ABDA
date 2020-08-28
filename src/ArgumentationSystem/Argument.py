from Configuration import Configuration
from KnowledgeBase.DefeasibleRule import DefeasibleRule
from KnowledgeBase.DefeasibleRuleSet import DefeasibleRuleSet


class Argument(object):

    def __init__(self, rule, arguments=None):
        self.BuildFromArguments = arguments
        # ASPIC Definitions
        self.TopRule = rule
        self.Conclusion = rule.RightSide
        self.Sub = set()
        if arguments:
            for arg in arguments:
                self.Sub = self.Sub.union(arg.Sub)
        self.Sub.add(self)
        self.DefRules = DefeasibleRuleSet()
        if arguments:
            for arg in arguments:
                self.DefRules.update(arg.DefRules)
        if isinstance(rule, DefeasibleRule):
            self.DefRules.add(rule)
        self.LastDefRules = DefeasibleRuleSet()
        if isinstance(rule, DefeasibleRule):
            self.LastDefRules.add(rule)
        elif arguments:
            for arg in arguments:
                self.LastDefRules.update(arg.LastDefRules)
        # Graph/Argumentation System properties
        self.AttacksArguments = set()
        self.AttackedFromArguments = set()
        self.Flattened = self.get_flattened_tree(self.TopRule)

    def get_flattened_tree(self, rule):
        output_string = "=>" if isinstance(rule, DefeasibleRule) else "->"
        output_string += rule.RightSide
        left_side_string = []
        for condition in rule.LeftSide:
            for s in self.BuildFromArguments:
                if s.Conclusion == condition:
                    left_side_string.append(f"({s.Flattened})")
                    break
        if left_side_string:
            if len(left_side_string) > 1:
                output_string = "(" + ",".join(left_side_string) + ")" + output_string
            else:
                output_string = left_side_string[0] + output_string
        return output_string

    def __le__(self, other):
        if Configuration.WeakestLink:
            return self.DefRules <= other.DefRules
        else:
            return self.LastDefRules <= other.LastDefRules

    def __lt__(self, other):
        return self <= other and not other <= self

    def __str__(self):
        if not self.Flattened: 
            self.Flattened = self.get_flattened_tree(self.TopRule)
        return str(self.Flattened)

    def __hash__(self):
        hash_string = ""
        if self.BuildFromArguments:
            for a in self.BuildFromArguments:
                hash_string += str(a.TopRule)
        hash_string += str(self.TopRule)
        return hash(hash_string)

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()
