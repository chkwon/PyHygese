import numpy as np
from hygese import AlgorithmParameters, Solver


def get_data():
    data = dict()
    data['distance_matrix'] = [
        [0, 548, 776, 696, 582, 274, 502, 194, 308, 194, 536, 502, 388, 354, 468, 776, 662],
        [548, 0, 684, 308, 194, 502, 730, 354, 696, 742, 1084, 594, 480, 674, 1016, 868, 1210],
        [776, 684, 0, 992, 878, 502, 274, 810, 468, 742, 400, 1278, 1164, 1130, 788, 1552, 754],
        [696, 308, 992, 0, 114, 650, 878, 502, 844, 890, 1232, 514, 628, 822, 1164, 560, 1358],
        [582, 194, 878, 114, 0, 536, 764, 388, 730, 776, 1118, 400, 514, 708, 1050, 674, 1244],
        [274, 502, 502, 650, 536, 0, 228, 308, 194, 240, 582, 776, 662, 628, 514, 1050, 708],
        [502, 730, 274, 878, 764, 228, 0, 536, 194, 468, 354, 1004, 890, 856, 514, 1278, 480],
        [194, 354, 810, 502, 388, 308, 536, 0, 342, 388, 730, 468, 354, 320, 662, 742, 856],
        [308, 696, 468, 844, 730, 194, 194, 342, 0, 274, 388, 810, 696, 662, 320, 1084, 514],
        [194, 742, 742, 890, 776, 240, 468, 388, 274, 0, 342, 536, 422, 388, 274, 810, 468],
        [536, 1084, 400, 1232, 1118, 582, 354, 730, 388, 342, 0, 878, 764, 730, 388, 1152, 354],
        [502, 594, 1278, 514, 400, 776, 1004, 468, 810, 536, 878, 0, 114, 308, 650, 274, 844],
        [388, 480, 1164, 628, 514, 662, 890, 354, 696, 422, 764, 114, 0, 194, 536, 388, 730],
        [354, 674, 1130, 822, 708, 628, 856, 320, 662, 388, 730, 308, 194, 0, 342, 422, 536],
        [468, 1016, 788, 1164, 1050, 514, 514, 662, 320, 274, 388, 650, 536, 342, 0, 764, 194],
        [776, 868, 1552, 560, 674, 1050, 1278, 742, 1084, 810, 1152, 274, 388, 422, 764, 0, 798],
        [662, 1210, 754, 1358, 1244, 708, 480, 856, 514, 468, 354, 844, 730, 536, 194, 798, 0]
    ]
    data['num_vehicles'] = 4
    data['depot'] = 0
    data['demands'] = [0, 1, 1, 2, 4, 2, 4, 8, 8, 1, 2, 1, 2, 4, 4, 8, 8]
    data['vehicle_capacity'] = 15  # different from OR-Tools: homogeneous capacity
    return data


def test_cvrp():
    data = get_data()

    # Solver initialization
    ap = AlgorithmParameters()
    ap.timeLimit = 1.1
    hgs_solver = Solver(ap, True)

    # Solve
    result = hgs_solver.solve_cvrp(data)
    print(result.cost)
    print(result.routes)
    assert (result.cost == 6208)


def test_cvrp_inputs():
    data = get_data()

    # Solver initialization
    ap = AlgorithmParameters(timeLimit=1.1)
    hgs_solver = Solver(parameters=ap, verbose=True)

    # Solve
    result = hgs_solver.solve_cvrp(data)
    print(result.cost)
    print(result.routes)
    assert (result.cost == 6208)


def test_cvrp_dist_mtx():
    # Solver initialization
    ap = AlgorithmParameters(timeLimit=3.1)
    hgs_solver = Solver(parameters=ap, verbose=True)

    data = dict()
    n = 17
    x = np.random.rand(n) * 1000
    y = np.random.rand(n) * 1000
    data['x_coordinates'] = x
    data['y_coordinates'] = y

    data['depot'] = 0
    data['demands'] = [0, 1, 1, 2, 4, 2, 4, 8, 8, 1, 2, 1, 2, 4, 4, 8, 8]
    data['vehicle_capacity'] = 15  # different from OR-Tools: homogeneous capacity

    # Solve with calculated distances
    dist_mtx = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            dist_mtx[i][j] = np.sqrt(
                np.square(x[i] - x[j]) + np.square(y[i] - y[j])
            )
    data['distance_matrix'] = dist_mtx
    result1 = hgs_solver.solve_cvrp(data)

    # solve without distance_matrix
    data.pop("distance_matrix", None)
    result2 = hgs_solver.solve_cvrp(data, rounding=False)
    assert abs(result1.cost - result2.cost) < 1e-3


def test_cvrp_duration():
    n = 10
    data = dict()
    data['x_coordinates'] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    data['y_coordinates'] = [5, 4, 3, 2, 1, 9, 8, 7, 6, 5]
    data['demands'] = [0, 2, 3, 1, 2, 3, 1, 2, 3, 1]
    data['vehicle_capacity'] = 10
    data['duration_limit'] = 18
    data['num_vehicles'] = 5

    # Solver initialization
    ap = AlgorithmParameters(timeLimit=1.1, seed=12, useSwapStar=True)
    hgs_solver = Solver(parameters=ap, verbose=True)

    result = hgs_solver.solve_cvrp(data, rounding=True)
    assert result.cost == 42
