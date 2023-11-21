from os import listdir
from os.path import isfile, join
import json

import pandas as pd

def run(dir):
    results = list()
    files = [join(dir, f) for f in listdir(dir) if isfile(join(dir, f))]
    for file in files:
        with open(file, "r") as file:
            results.append(json.load(file))
    df = pd.DataFrame(results)
    df.to_excel("{}/results.xlsx".format(dir), index=False)

if __name__ == "__main__":
    path = "./results/results-n10-n20-a2-Linf/"
    run(path)