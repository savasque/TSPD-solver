
import sys

from classes.instance import Instance
from solver.solver import solve
from data import instance_generator as ins_gen
from data.parser import write_instance, write_results, parse_custom

# if len(sys.argv) != 5:
#     sys.exit('Incorrect number of params. Please execute solver as \'python main.py <n> <alpha> <L> <instance_number>\'')
# n, alpha, L, seed = list(map(int, sys.argv[1:]))

for n in range(11, 20):
    for alpha in [1, 2, 3]:
        for L in ["inf"]:
            for seed in range(1, 11):
                # for L in [20, 40, 60, 100, 150, 200]:
                # L = float("inf")
                # nodes, c, d, pos = ins_gen.run(n, alpha, seed=seed)
                # instance = Instance(seed, nodes, alpha, L, c, d)
                # write_instance(instance)

                file_name = "./data/instances_custom/n{}_a{}_L{}_{}.json".format(n, alpha, L, seed)
                instance = parse_custom(file_name)
                results = solve(instance)
                write_results(instance, results)

# print()

