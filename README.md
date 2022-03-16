# pyhgscvrp

A Python wrapper for [HGS-CVRP](https://github.com/vidalt/HGS-CVRP).

Installation requires a `C++` compiler and `cmake` tool.
Download this repository and run `pip install .`
For example:
```
git clone git@github.com:chkwon/pyhgscvrp.git
cd pyhgscvrp
pip install .
```

Example codes are found in `/examples`.

```
python3 examples/tsp.py
python3 examples/cvrp.py
```

CVRP:
```python
import numpy as np 
from hgs import AlgorithmParameters, Solver

n = 20
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

# You may also supply distance_matrix instead of coordinates, or in addition to coordinates
# If you supply distance_matrix, it will be used for cost calculation.
# The additional coordinates will be helpful in speeding up the algorithm.
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
```