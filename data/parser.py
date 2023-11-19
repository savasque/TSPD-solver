
from os import listdir
from os.path import isfile, join
import json
import numpy as np

from classes.instance import Instance
from classes.node import Node

def parse_agatz(n):
    path = './data/instances_agatz/uniform'
    files = [join(path, f) for f in listdir(path) if isfile(join(path, f)) and f[:-4].split('-')[-1] == 'n{}'.format(n) and len(f[:-4].split("-")) == 3]
    instances = list()
    counter = 0
    for f in files:
        counter += 1
        with open(f, 'r') as data:
            data = data.readlines()
            # alpha = int(float(data[1]) / float(data[3]))
            (depot_x, depot_y, _) = data[7].split(' ')
            depot = Node(1, float(depot_x), float(depot_y))
            nodes = [depot]
            node_id = 1
            for i in data[9:]:
                node_id += 1
                (x, y, _) = i.split(' ')
                node = Node(node_id, float(x), float(y))
                nodes.append(node)
            nodes.append(Node(n + 1, depot.x, depot.y))

            truck_travel_time = {
                (i, j): int(np.sqrt((i.x - j.x) ** 2 + (i.y - j.y) ** 2) * 10) / 10
                for i in nodes for j in nodes if i != j
            }
            drone_travel_time = {
                (i, j): truck_travel_time[i, j] / 2
                for (i, j) in truck_travel_time
            }
            instance = Instance(counter, nodes, 2, float("inf"), truck_costs=truck_travel_time, drone_costs=drone_travel_time)
            instances.append(instance)

    return instances

def parse_poikonen(n):
    #path = './data/instances_poikonen/Table4LocationsFull.csv'
    #data = pd.read_csv(path, header)
    #print()
    pass

def parse_custom(file_name, alpha=None, L=None, R=None):
    with open(file_name, "r") as file:
        data = json.load(file)
        if data["drone_range"] == "inf": data["drone_range"] = float("inf")
        nodes = [Node(1, data["depot_location"][0], data["depot_location"][1])]
        for id, pos in data["customer_locations"].items():
            nodes.append(Node(int(id), pos[0], pos[1]))
        nodes.append(Node(data["number_of_nodes"] + 1, data["depot_location"][0], data["depot_location"][1]))
        truck_travel_time = {
            (i, j): int(np.sqrt((i.x - j.x) ** 2 + (i.y - j.y) ** 2) * 10) / 10
            for i in nodes for j in nodes if i != j
        }
        drone_travel_time = {
            (i, j): truck_travel_time[i, j] / alpha
            for (i, j) in truck_travel_time
        }
        L = R / 100 * max(drone_travel_time.values())
        instance = Instance(data["id"], nodes, alpha, L, truck_costs=truck_travel_time, drone_costs=drone_travel_time)
    
    return instance


def write_instance(instance):
    data = {
        "id": instance.id,
        "truck_speed": 1,
        "drone_speed": instance.alpha,
        "drone_range": instance.L if instance.L < float("inf") else "inf",
        "number_of_nodes": len(instance.nodes) - 1,
        "depot_location": (instance.nodes[0].x, instance.nodes[0].y),
        "customer_locations": {
            node.id: (node.x, node.y)
            for node in instance.nodes if node.id not in [1, len(instance.nodes)]
        }
    }
    
    with open("./data/instances_custom/n{}_{}.json".format(
        data["number_of_nodes"],
        data["id"]
    ), "w") as file:
        json.dump(data, file)

def write_results(instance, results):
    with open("./results/n{}_a{}_L{}_{}.json".format(
        len(instance.nodes) - 1,
        instance.alpha,
        instance.L,
        instance.id
    ), "w") as file:
        json.dump(results, file)