from KnowledgeBase.RuleCollection import RuleCollection
from KnowledgeBase.DefeasibleRule import DefeasibleRule
from KnowledgeBase.StrictRule import StrictRule


def load_rules(path):
    file = open(path, "r")
    rules = RuleCollection()
    current_strength = 1
    line = file.readline()
    while line:
        if line.startswith("#"):
            line = file.readline()
            continue
        # newline -> block ended, increment strength value
        if line == "\n":
            current_strength += 1
            line = file.readline()
            continue
        try:
            rules.StrictRules.add(StrictRule.parse(line))
        except:
            rules.DefeasibleRules.add(DefeasibleRule.parse(line, current_strength))
        line = file.readline()
    file.close()
    return rules
