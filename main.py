
import sys
from argparse import ArgumentParser

from classes.instance import Instance
from solver.solver import solve
from data import instance_generator as ins_gen
from data.parser import write_instance, write_results, parse_custom, parse_agatz

# instances = parse_agatz(20)
# for instance in instances:
#     write_instance(instance)

def run(args):
    n, alpha, L, seed = args.nodes, args.alpha, args.range, args.seed
    # for seed in range(1, seeds + 1):
    # # L = float("inf")
    # # alpha = 2
    # nodes, c, d, pos = ins_gen.run(n, alpha, seed=seed)
    # instance = Instance(seed, nodes, alpha, L, c, d)
    # write_instance(instance)

    if not alpha:
        alpha = 2
    if not L:
        L = float("inf")
    file_name = "./data/instances_custom/n{}_{}.json".format(n, seed)
    instance = parse_custom(file_name, alpha, L)
    results = solve(instance)
    write_results(instance, results)

if __name__ == "__main__":
    argparse = ArgumentParser()
    argparse.add_argument(
        "-n", "--nodes", type=int
    )
    argparse.add_argument(
        "-a", "--alpha", type=int
    )
    argparse.add_argument(
        "-L", "--range", type=int
    )
    argparse.add_argument(
        "-s", "--seed", type=int
    )
    args = argparse.parse_args()
    run(args)
