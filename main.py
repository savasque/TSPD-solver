
import sys

from classes.instance import Instance
from solver.solver import solve
from data import instance_generator as ins_gen
from data.parser import write_instance, write_results, parse_custom, parse_agatz

# instances = parse_agatz(20)
# for instance in instances:
#     write_instance(instance)

if len(sys.argv) != 5:
    sys.exit('Incorrect number of params. Please execute solver as \'python main.py <n> <alpha> <L> <instance_number>\'')
n, alpha, L, seeds = list(map(int, sys.argv[1:]))

for seed in range(1, seeds + 1):
    # # L = float("inf")
    # # alpha = 2
    # nodes, c, d, pos = ins_gen.run(n, alpha, seed=seed)
    # instance = Instance(seed, nodes, alpha, L, c, d)
    # write_instance(instance)

    file_name = "./data/instances_custom/n{}_{}.json".format(n, seed)
    instance = parse_custom(file_name, alpha, L)
    instance.L = L
    results = solve(instance)
    write_results(instance, results)

