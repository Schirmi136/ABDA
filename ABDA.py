from Configuration import Configuration
from ABDAShell import ABDAShell
from ArgumentationSystem.ArgumentBuilder import build_arguments
from ArgumentationSystem.ArgumentBuilder import build_attacks
from KnowledgeBase.AspicRulesLoader import load_rules
from ArgumentationSystem.ArgumentationGraph import ArgumentationGraph
import argparse


if __name__ == "__main__":
    # Read in command line arguments
    parser = argparse.ArgumentParser(description='Argument-Based Discussion using ASPIC')

    parser.add_argument("-file", help="path to file containing the rules",
                        default="rules.txt")

    linkGroup = parser.add_mutually_exclusive_group(required=True)
    linkGroup.add_argument("-wl", help="weakest link principle", action="store_true")
    linkGroup.add_argument("-ll", help="last link principle", action="store_true")

    linkGroup = parser.add_mutually_exclusive_group(required=True)
    linkGroup.add_argument("-do", help="democratic order", action="store_true")
    linkGroup.add_argument("-eo", help="elitist order", action="store_true")

    parser.add_argument("-tp", help="close strict rules under transposition", action="store_true")
    parser.add_argument("-verbose", help="print additional information while constrocting argumentation graph", action="store_true")

    args = parser.parse_args()

    # Set configuration (so DefeasibleRuleCollection and Argument can access it)
    Configuration.DemocraticOrder = args.do
    Configuration.WeakestLink = args.wl
    Configuration.Verbose = args.verbose

    # Load rules from file
    print("Loading rules...")
    rules = load_rules(args.file)
    if not args.tp and not rules.is_closed_under_transposition():
        print("WARNING: strict rules are not closed under transposition")
    if args.tp:
        rules.close_under_transposition()

    # Build argumentation system
    print("Building argumentation system...")
    arguments = build_arguments(rules.get_all_rules())
    attacks = build_attacks(arguments)
    graph = ArgumentationGraph(arguments, attacks)

    # Compute grounded extension and minMax - Numbering
    groundedLabelling = graph.get_grounded_labelling()
    minMaxNumbering = graph.get_min_max(groundedLabelling)

    # Start shell for user interaction
    shell = ABDAShell(graph, groundedLabelling, minMaxNumbering)
    shell.cmdloop()
