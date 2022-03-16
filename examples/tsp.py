import numpy as np 
from hgs import AlgorithmParameters, Solver

def tsp_by_coordinates(n):
    x = (np.random.rand(n) * 1000)
    y = (np.random.rand(n) * 1000)
    verbose = False

    # data preparation
    data = {}
    data['x_coordinates'] = x
    data['y_coordinates'] = y

    # Solver initialization
    ap = AlgorithmParameters()
    ap.timeLimit = 1.3 # seconds
    hgs_solver = Solver(ap, verbose)

    # solve TSP using coordinates only
    result = hgs_solver.solve_tsp(data)
    print(result.cost)
    print(result.routes)

def tsp_by_dist_mtx(n):
    x = (np.random.rand(n) * 1000)
    y = (np.random.rand(n) * 1000)
    verbose = False

    # data preparation
    data = {}
    dist_mtx = np.round(np.random.rand(n, n) * 1000)
    for i in range(n):
        for j in range(n):
            dist_mtx[i][j] = np.math.sqrt(
                (x[i] - x[j]) ** 2 + (y[i] - y[j]) ** 2
            )
    data['distance_matrix'] = dist_mtx

    # Solver initialization
    ap = AlgorithmParameters()
    ap.timeLimit = 1.3 # seconds

    # solve TSP using by dist_mtx only
    hgs_solver = Solver(ap, verbose)
    result = hgs_solver.solve_tsp(data)
    print(result.cost)
    print(result.routes)


def tsp_by_both(n):
    x = (np.random.rand(n) * 1000)
    y = (np.random.rand(n) * 1000)
    verbose = False

    # data preparation
    data = {}
    data['x_coordinates'] = x
    data['y_coordinates'] = y

    dist_mtx = np.round(np.random.rand(n, n) * 1000)
    for i in range(n):
        for j in range(n):
            dist_mtx[i][j] = np.math.sqrt(
                (x[i] - x[j]) ** 2 + (y[i] - y[j]) ** 2
            )
    data['distance_matrix'] = dist_mtx

    # Solver initialization
    ap = AlgorithmParameters()
    ap.timeLimit = 1.3 # seconds

    # solve TSP using both coordinates and dist_mtx
    hgs_solver = Solver(ap, verbose)
    result = hgs_solver.solve_tsp(data)
    print(result.cost)
    print(result.routes)


if __name__ == '__main__':
    n = 20
    tsp_by_coordinates(n)
    tsp_by_dist_mtx(n)
    tsp_by_both(n)