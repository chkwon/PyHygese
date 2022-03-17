import numpy as np 
from hygese import AlgorithmParameters, Solver

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

def tsp_ortools():
    data = {}
    data['distance_matrix'] = [
        [0, 2451, 713, 1018, 1631, 1374, 2408, 213, 2571, 875, 1420, 2145, 1972],
        [2451, 0, 1745, 1524, 831, 1240, 959, 2596, 403, 1589, 1374, 357, 579],
        [713, 1745, 0, 355, 920, 803, 1737, 851, 1858, 262, 940, 1453, 1260],
        [1018, 1524, 355, 0, 700, 862, 1395, 1123, 1584, 466, 1056, 1280, 987],
        [1631, 831, 920, 700, 0, 663, 1021, 1769, 949, 796, 879, 586, 371],
        [1374, 1240, 803, 862, 663, 0, 1681, 1551, 1765, 547, 225, 887, 999],
        [2408, 959, 1737, 1395, 1021, 1681, 0, 2493, 678, 1724, 1891, 1114, 701],
        [213, 2596, 851, 1123, 1769, 1551, 2493, 0, 2699, 1038, 1605, 2300, 2099],
        [2571, 403, 1858, 1584, 949, 1765, 678, 2699, 0, 1744, 1645, 653, 600],
        [875, 1589, 262, 466, 796, 547, 1724, 1038, 1744, 0, 679, 1272, 1162],
        [1420, 1374, 940, 1056, 879, 225, 1891, 1605, 1645, 679, 0, 1017, 1200],
        [2145, 357, 1453, 1280, 586, 887, 1114, 2300, 653, 1272, 1017, 0, 504],
        [1972, 579, 1260, 987, 371, 999, 701, 2099, 600, 1162, 1200, 504, 0],
    ]  # yapf: disable

        # Solver initialization
    ap = AlgorithmParameters()
    ap.timeLimit = 0.8 # seconds

    # solve TSP using both coordinates and dist_mtx
    hgs_solver = Solver(ap, True)
    result = hgs_solver.solve_tsp(data)
    print(result.cost)
    print(result.routes)

if __name__ == '__main__':
    n = 20
    tsp_by_coordinates(n)
    tsp_by_dist_mtx(n)
    tsp_by_both(n)
    tsp_ortools()