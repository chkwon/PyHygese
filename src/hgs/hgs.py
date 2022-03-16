import os 
basedir = os.path.abspath(os.path.dirname(__file__))
HGS_LIBRARY_FILEPATH = os.path.join(basedir, 'libhgscvrp.dylib')

from ctypes import Structure, CDLL, POINTER, c_int, c_double, c_char, sizeof, cast, byref
import numpy as np

c_double_p = POINTER(c_double)
c_int_p = POINTER(c_int)
c_int_max = 2 ** (sizeof(c_int) * 8 - 1) - 1


class AlgorithmParameters(Structure):
    _fields_ = [("nbGranular", c_int),
                ("mu", c_int),
                ("lambda", c_int),
                ("nbElite", c_int),
                ("nbClose", c_int),
                ("targetFeasible", c_double),
                ("penaltyIncrease", c_double),
                ("penaltyDecrease", c_double),
                ("repairProb", c_double),
                ("seedRNG", c_int),
                ("nbIter", c_int),
                ("timeLimit", c_double),
                ("isRoundingInteger", c_char)]

    def __init__(self):
        # HGS default values
        super().__init__(20, 25, 40, 4, 5, 0.2, 1.20, 0.85, 0.5, 1, 20000, c_double(c_int_max), True)


class _SolutionRoute(Structure):
    _fields_ = [("length", c_int),
                ("path", c_int_p)]


class _Solution(Structure):
    _fields_ = [("cost", c_double),
                ("time", c_double),
                ("n_routes", c_int),
                ("routes", POINTER(_SolutionRoute))]


class RoutingSolution:
    def __init__(self, sol_ptr):
        if not sol_ptr:
            raise TypeError("The solution pointer is null.")

        self.cost = sol_ptr[0].cost
        self.time = sol_ptr[0].time
        self.n_routes = sol_ptr[0].n_routes
        self.routes = []
        for i in range(self.n_routes):
            r = sol_ptr[0].routes[i]
            path = r.path[0:r.length]
            self.routes.append(path)


class Solver:
    def __init__(self,
                 algorithm_parameters: AlgorithmParameters,
                 verbose: bool):
        hgs_library = CDLL(HGS_LIBRARY_FILEPATH)

        self.algorithm_parameters = algorithm_parameters
        self.verbose = verbose

        # solve_cvrp
        self._c_api_solve_cvrp = hgs_library.solve_cvrp
        self._c_api_solve_cvrp.argtypes = [c_int, c_double_p, c_double_p, c_double_p, c_double_p,
                                           c_int, c_int, POINTER(AlgorithmParameters), c_char]
        self._c_api_solve_cvrp.restype = POINTER(_Solution)

        # solve_cvrp_dist_mtx
        self._c_api_solve_cvrp_dist_mtx = hgs_library.solve_cvrp_dist_mtx
        self._c_api_solve_cvrp_dist_mtx.argtypes = [c_int, c_double_p, c_double_p, c_double_p, c_double_p, c_double_p,
                                                    c_int, c_int, POINTER(AlgorithmParameters), c_char]
        self._c_api_solve_cvrp_dist_mtx.restype = POINTER(_Solution)

        # delete_solution
        self._c_api_delete_sol = hgs_library.delete_solution
        self._c_api_delete_sol.restype = None
        self._c_api_delete_sol.argtypes = [POINTER(_Solution)]

    def solve_cvrp(self, data):
        if data['depot'] != 0:
            raise ValueError("In HGS, the depot location must be 0.")

        # required data
        demand = np.asarray(data['demands'])
        n_nodes = len(demand)
        vehicle_capacity = data['vehicle_capacity']
        maximum_number_of_vehicles = data['num_vehicles']

        # optional service time
        service_time = data.get('service_time')
        if service_time is None:
            service_time = np.zeros(n_nodes)
        else:
            service_time = np.asarray(service_time)

        x_coords = data.get('x_coordinates')
        y_coords = data.get('y_coordinates')
        dist_mtx = data.get('distance_matrix')

        if x_coords is None or y_coords is None:
            assert (dist_mtx is not None)
            x_coords = np.zeros(n_nodes)
            y_coords = np.zeros(n_nodes)
        else:
            x_coords = np.asarray(x_coords)
            y_coords = np.asarray(y_coords)

        assert (len(x_coords) == len(y_coords) == len(service_time) == len(demand))
        assert (x_coords >= 0.0).all()
        assert (y_coords >= 0.0).all()
        assert (service_time >= 0.0).all()
        assert (demand >= 0.0).all()

        if dist_mtx is not None:
            dist_mtx = np.asarray(dist_mtx)
            assert (dist_mtx.shape[0] == dist_mtx.shape[1])
            assert (dist_mtx >= 0.0).all()
            return self._solve_cvrp_dist_mtx(x_coords,
                                             y_coords,
                                             dist_mtx,
                                             service_time,
                                             demand,
                                             vehicle_capacity,
                                             maximum_number_of_vehicles,
                                             self.algorithm_parameters,
                                             self.verbose)
        else:
            return self._solve_cvrp(x_coords,
                                    y_coords,
                                    service_time,
                                    demand,
                                    vehicle_capacity,
                                    maximum_number_of_vehicles,
                                    self.algorithm_parameters,
                                    self.verbose)

    def solve_tsp(self, data):
        x_coords = data.get('x_coordinates')
        dist_mtx = data.get('distance_matrix')
        if dist_mtx is None:
            n_nodes = x_coords.size
        else:
            dist_mtx = np.asarray(dist_mtx)
            n_nodes = dist_mtx.shape[0]

        data['num_vehicles'] = 1
        data['depot'] = 0
        data['demands'] = np.ones(n_nodes)
        data['vehicle_capacity'] = n_nodes
        data['service_time'] = np.zeros(n_nodes)
        
        return self.solve_cvrp(data)

    def _solve_cvrp(self,
                    x_coords: np.ndarray,
                    y_coords: np.ndarray,
                    service_time: np.ndarray,
                    demand: np.ndarray,
                    vehicle_capacity: int,
                    maximum_number_of_vehicles: int,
                    algorithm_parameters: AlgorithmParameters,
                    verbose: bool):
        n_nodes = x_coords.size
        x_ct = x_coords.astype(c_double).ctypes
        y_ct = y_coords.astype(c_double).ctypes
        s_ct = service_time.astype(c_double).ctypes
        d_ct = demand.astype(c_double).ctypes

        sol_p = self._c_api_solve_cvrp(n_nodes,
                                       cast(x_ct, c_double_p),
                                       cast(y_ct, c_double_p),
                                       cast(s_ct, c_double_p),
                                       cast(d_ct, c_double_p),
                                       vehicle_capacity,
                                       maximum_number_of_vehicles,
                                       byref(algorithm_parameters),
                                       verbose)

        result = RoutingSolution(sol_p)
        self._c_api_delete_sol(sol_p)
        return result

    def _solve_cvrp_dist_mtx(self,
                             x_coords: np.ndarray,
                             y_coords: np.ndarray,
                             dist_mtx: np.ndarray,
                             service_time: np.ndarray,
                             demand: np.ndarray,
                             vehicle_capacity: int,
                             maximum_number_of_vehicles: int,
                             algorithm_parameters: AlgorithmParameters,
                             verbose: bool):
        n_nodes = x_coords.size

        x_ct = x_coords.astype(c_double).ctypes
        y_ct = y_coords.astype(c_double).ctypes
        s_ct = service_time.astype(c_double).ctypes
        d_ct = demand.astype(c_double).ctypes

        m_ct = dist_mtx.reshape(n_nodes * n_nodes).astype(c_double).ctypes

        sol_p = self._c_api_solve_cvrp_dist_mtx(n_nodes,
                                                cast(x_ct, c_double_p),
                                                cast(y_ct, c_double_p),
                                                cast(m_ct, c_double_p),
                                                cast(s_ct, c_double_p),
                                                cast(d_ct, c_double_p),
                                                vehicle_capacity, maximum_number_of_vehicles,
                                                byref(algorithm_parameters), verbose)

        result = RoutingSolution(sol_p)
        self._c_api_delete_sol(sol_p)
        return result
