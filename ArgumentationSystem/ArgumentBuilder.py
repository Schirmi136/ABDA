from ArgumentationSystem.Argument import Argument
from KnowledgeBase.DefeasibleRule import DefeasibleRule
from ArgumentationSystem.Attack import Attack
from Configuration import Configuration


def get_applicable_arguments(rule, arguments, used_arguments):
    args = set()
    for condition in rule.LeftSide:
        arg = list(filter(lambda a: a.Conclusion == condition and a not in used_arguments, arguments))
        if not arg:
            return None
        args.add(arg[0])
    return args


def build_arguments(rules):
    arguments = set()
    # Construct arguments with empty left side
    for rule in set(filter(lambda r: not r.LeftSide, rules)):
        new_arg = Argument(rule)
        arguments.add(new_arg)

    old_arguments = set()
    while len(old_arguments) != len(arguments):
        old_arguments = arguments.copy()
        for rule in rules:
            if rule.LeftSide:
                used_arguments = set()
                args = get_applicable_arguments(rule, arguments, used_arguments)
                while args:
                    new_arg = Argument(rule, args)
                    if new_arg not in arguments:
                        arguments.add(Argument(rule, args))
                    used_arguments = used_arguments.union(args)
                    args = get_applicable_arguments(rule, arguments, used_arguments)
    return arguments


def build_attacks(arguments):
    attacks = set()
    for a in arguments:
        for b in arguments:
            if does_attacks(a, b):
                attacks.add(Attack(a, b))
    return attacks


def does_attacks(a, b):
    # Undercutting?
    for b1 in b.Sub:
        if isinstance(b1.TopRule, DefeasibleRule) and is_negation(b1.TopRule.Name, a.Conclusion):
            if Configuration.Verbose:
                print(str(a) + " undercuts " + str(b) + " on " + str(b1.TopRule.Name))
            return True
    # Rebutting?
    for b1 in b.Sub:
        if is_negation(a.Conclusion, b1.Conclusion) and not a < b1:
            if Configuration.Verbose:
                print(str(a) + " rebuts " + str(b) + " on " + str(b1))
            return True
    return False


def is_negation(a, b):
    return a == "-" + b or b == "-" + a
