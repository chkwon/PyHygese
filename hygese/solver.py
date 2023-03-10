from .wrapper import _solve_cvrp_dist_mtx, _solve_cvrp, RoutingSolution
from dataclasses import dataclass
import numpy as np

from ctypes import c_int, sizeof
import sys
    
C_INT_MAX = 2 ** (sizeof(c_int) * 8 - 1) - 1
C_DBL_MAX = sys.float_info.max


@dataclass
class AlgorithmParameters:
    nbGranular: int = 20
    mu: int = 25
    lambda_: int = 40
    nbElite: int = 4
    nbClose: int = 5
    targetFeasible: float = 0.2
    seed: int = 0
    nbIter: int = 20000
    timeLimit: float = 0.0
    useSwapStar: bool = True
    

class Solver:
    def __init__(self, parameters=AlgorithmParameters(), verbose=True):
        self.algorithm_parameters = parameters
        self.verbose = verbose

    def solve_cvrp(self, data, rounding=True):
        # required data
        demand = np.asarray(data["demands"]).astype(np.float64)
        vehicle_capacity = data["vehicle_capacity"]
        n_nodes = len(demand)

        # optional depot
        depot = data.get("depot", 0)
        if depot != 0:
            raise ValueError("In HGS, the depot location must be 0.")

        # optional num_vehicles
        maximum_number_of_vehicles = data.get("num_vehicles", C_INT_MAX)

        # optional service_times
        service_times = data.get("service_times")
        if service_times is None:
            service_times = np.zeros(n_nodes).astype(np.float64)
        else:
            service_times = np.asarray(service_times).astype(np.float64)

        # optional duration_limit
        duration_limit = data.get("duration_limit")
        if duration_limit is None:
            is_duration_constraint = False
            duration_limit = C_DBL_MAX
        else:
            is_duration_constraint = True

        is_rounding_integer = rounding

        x_coords = data.get("x_coordinates")
        y_coords = data.get("y_coordinates")
        dist_mtx = data.get("distance_matrix")

        if x_coords is None or y_coords is None:
            assert dist_mtx is not None
            x_coords = np.zeros(n_nodes).astype(np.float64)
            y_coords = np.zeros(n_nodes).astype(np.float64)
        else:
            x_coords = np.asarray(x_coords).astype(np.float64)
            y_coords = np.asarray(y_coords).astype(np.float64)

        assert len(x_coords) == len(y_coords) == len(service_times) == len(demand)
        assert (x_coords >= 0.0).all()
        assert (y_coords >= 0.0).all()
        assert (service_times >= 0.0).all()
        assert (demand >= 0.0).all()

        if dist_mtx is not None:
            dist_mtx = np.asarray(dist_mtx).astype(np.float64)
            assert dist_mtx.shape[0] == dist_mtx.shape[1]
            assert (dist_mtx >= 0.0).all()
            
            dist_mtx = dist_mtx.reshape((n_nodes * n_nodes, ))
            
            print("shape = " , dist_mtx.shape) 
            
            return _solve_cvrp_dist_mtx(
                x_coords,
                y_coords,
                dist_mtx,
                service_times,
                demand,
                vehicle_capacity,
                duration_limit,
                is_duration_constraint,
                maximum_number_of_vehicles,
                self.algorithm_parameters.nbGranular,
                self.algorithm_parameters.mu,
                self.algorithm_parameters.lambda_,
                self.algorithm_parameters.nbElite,
                self.algorithm_parameters.nbClose,
                self.algorithm_parameters.targetFeasible,
                self.algorithm_parameters.seed,
                self.algorithm_parameters.nbIter,
                self.algorithm_parameters.timeLimit,
                self.algorithm_parameters.useSwapStar,
                self.verbose,
            )
        else:
            return _solve_cvrp(
                x_coords,
                y_coords,
                service_times,
                demand,
                vehicle_capacity,
                duration_limit,
                is_rounding_integer,
                is_duration_constraint,
                maximum_number_of_vehicles,
                self.algorithm_parameters.nbGranular,
                self.algorithm_parameters.mu,
                self.algorithm_parameters.lambda_,
                self.algorithm_parameters.nbElite,
                self.algorithm_parameters.nbClose,
                self.algorithm_parameters.targetFeasible,
                self.algorithm_parameters.seed,
                self.algorithm_parameters.nbIter,
                self.algorithm_parameters.timeLimit,
                self.algorithm_parameters.useSwapStar,
                self.verbose,
            )

    def solve_tsp(self, data, rounding=True):
        x_coords = data.get("x_coordinates")
        dist_mtx = data.get("distance_matrix")
        if dist_mtx is None:
            n_nodes = x_coords.size
        else:
            dist_mtx = np.asarray(dist_mtx)
            n_nodes = dist_mtx.shape[0]

        data["num_vehicles"] = 1
        data["depot"] = 0
        data["demands"] = np.ones(n_nodes)
        data["vehicle_capacity"] = n_nodes

        return self.solve_cvrp(data, rounding=rounding)
