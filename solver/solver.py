
from classes.solution import Solution
from utils import plotter 
from solver.models.master_problem import MasterProblem
from solver.models.subproblem import SubProblem
from solver.callback import Callback
from solver.functions.solver_functions import get_route, get_route_recourse, get_shortcuts

from time import time

def solve(instance):
    master_problem_params = {
        'SEC': None,
        'activate_DB': True,
        'min_visited_nodes': 0,
        'time_limit': 3600
    }
    subproblem_params = {
        'M': sum(sorted(instance.truck_travel_time.values())[::-1][:2 * (instance.n - 1):2])
    }

    functions = {
        'get_route': get_route,
        'get_route_recourse': get_route_recourse,
        'get_shortcuts': get_shortcuts
    }
    if instance.alpha == 1:
        master_problem_params["min_visited_nodes"] = (len(instance.nodes) - 1) // 2 + 1

    master_problem = MasterProblem(instance, master_problem_params)
    subproblem = SubProblem(instance, subproblem_params)
    callback = Callback(instance, functions)
    solution = Solution(instance)

    cb = callback.callback(master_problem, subproblem, solution)
    
    solution.start_time = time()
    master_problem._solve(cb)
    
    solution.truck_arcs = [a for a in instance.arcs if master_problem.variables['x'][a].X > 0.5]
    recourse = get_route_recourse(solution.truck_arcs, instance.arcs)

    subproblem.set_constr_rhs(recourse)
    subproblem._solve()
    solution.operations = [e for e in instance.operations if subproblem.variables['o'][e].X > 0.5]

    # plotter.plot(instance, solution.truck_arcs, solution.drone_arcs)

    results = {
        "objval": master_problem.model.ObjVal, 
        "runtime": master_problem.model.runtime, 
        "mipgap": master_problem.model.MIPGap, 
        "is_model_optimal": 1 if master_problem.model.status == 2 else 0
    }

    return results

