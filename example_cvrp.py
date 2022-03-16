import numpy as np 
from hgs import AlgorithmParameters, Solver

def cvrp_example(n):
    x = (np.random.rand(n) * 1000)
    y = (np.random.rand(n) * 1000)
    verbose = True

    # Solver initialization
    ap = AlgorithmParameters()
    ap.timeLimit = 3.2
    hgs_solver = Solver(ap, verbose)

    # data preparation
    data = {}
    data['x_coordinates'] = x
    data['y_coordinates'] = y

    # you may also supply dixt_mtx instead of coordinates, or without coordinates
    # data['distance_matrix'] = dist_mtx

    data['service_time'] = np.zeros(n)
    demand = np.ones(n)
    demand[0] = 0 # depot demand = 0
    data['demand'] = demand
    data['vehicle_capacity'] = np.ceil(n/3).astype(int)
    data['num_vehicles'] = 3
    data['depot'] = 0

    result = hgs_solver.solve_cvrp(data)
    print(result.cost)
    print(result.routes)

if __name__ == '__main__':
    n = 20
    cvrp_example(n)
