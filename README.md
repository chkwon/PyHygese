# PyHygese

[![Build Status](https://github.com/chkwon/PyHygese/workflows/CI/badge.svg?branch=master)](https://github.com/chkwon/PyHygese/actions/workflows/ci.yml?query=workflow%3ACI)
[![codecov](https://codecov.io/gh/chkwon/PyHygese/branch/master/graph/badge.svg)](https://codecov.io/gh/chkwon/PyHygese)

*This package is under active development. It can introduce breaking changes anytime. Please use it at your own risk.*

**A solver for the Capacitated Vehicle Routing Problem (CVRP)**

This package provides a simple Python wrapper for the Hybrid Genetic Search solver for Capacitated Vehicle Routing Problems [(HGS-CVRP)](https://github.com/vidalt/HGS-CVRP) through [a C interface](https://github.com/chkwon/HGS-CVRP).

Installation requires `git`, `gcc`, `make`, and `cmake`. 
On Windows, for example, you can install them by `scoop install git gcc make cmake` using [Scoop](scoop.sh).
Then, install the PyHygese package:
```
python3 -m pip install git+https://github.com/chkwon/PyHygese
```


## CVRP Example (random)
```python
import numpy as np 
from hygese import AlgorithmParameters, Solver

n = 20
x = (np.random.rand(n) * 1000)
y = (np.random.rand(n) * 1000)

# Solver initialization
ap = AlgorithmParameters(timeLimit=3.2)  # seconds
hgs_solver = Solver(parameters=ap, verbose=True)

# data preparation
data = dict()
data['x_coordinates'] = x
data['y_coordinates'] = y

# You may also supply distance_matrix instead of coordinates, or in addition to coordinates
# If you supply distance_matrix, it will be used for cost calculation.
# The additional coordinates will be helpful in speeding up the algorithm.
# data['distance_matrix'] = dist_mtx

data['service_times'] = np.zeros(n)
demands = np.ones(n)
demands[0] = 0 # depot demand = 0
data['demands'] = demands
data['vehicle_capacity'] = np.ceil(n/3).astype(int)
data['num_vehicles'] = 3
data['depot'] = 0

result = hgs_solver.solve_cvrp(data)
print(result.cost)
print(result.routes)

```

**NOTE:** The `result.routes` above does not include the depot. All vehicles start from the depot and return to the depot.


## another CVRP example

```python
# A CVRP from https://developers.google.com/optimization/routing/cvrp
from hygese import AlgorithmParameters, Solver
import numpy as np 

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
data['service_times'] = np.zeros(len(data['demands']))

# Solver initialization
ap = AlgorithmParameters(timeLimit=3.2)  # seconds
hgs_solver = Solver(parameters=ap, verbose=True)

# Solve
result = hgs_solver.solve_cvrp(data)
print(result.cost)
print(result.routes)
```


## TSP example

```python
# A TSP example from https://developers.google.com/optimization/routing/tsp
from hygese import AlgorithmParameters, Solver

data = dict()
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
] 

# Solver initialization
ap = AlgorithmParameters(timeLimit=0.8)  # seconds
hgs_solver = Solver(parameters=ap, verbose=True)

# Solve
result = hgs_solver.solve_tsp(data)
print(result.cost)
print(result.routes)
```

## Algorithm Parameters
Configurable algorithm parameters are defined in the `AlgorithmParameters` dataclass with default values:
```python
@dataclass
class AlgorithmParameters:
    nbGranular: int = 20
    mu: int = 25
    lambda_: int = 40
    nbElite: int = 4
    nbClose: int = 5
    targetFeasible: float = 0.2
    seed: int = 1
    nbIter: int = 20000
    timeLimit: float = C_DBL_MAX 
    useSwapStar: bool = True
```
where `C_DBL_MAX = sys.float_info.max`.

## Others
A Julia wrapper is available: [Hygese.jl](https://github.com/chkwon/Hygese.jl)

