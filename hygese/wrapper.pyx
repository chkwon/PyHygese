cdef extern from "AlgorithmParameters.h":
    cdef struct AlgorithmParameters:
        int nbGranular
        int mu
        int lambda_ "lambda"
        int nbElite
        int nbClose
        double targetFeasible
        int seed
        int nbIter
        double timeLimit
        int useSwapStar

cdef extern from "C_Interface.h":
    cdef struct SolutionRoute:
        int length
        int *path
    
    cdef struct Solution:
        double cost
        double time
        int n_routes
        SolutionRoute *routes
    
    # Define the C functions in Cython syntax
    Solution* solve_cvrp(int n, double* x, double* y, double* serv_time, double* dem,
                        double vehicleCapacity, double durationLimit, char isRoundingInteger, char isDurationConstraint,
                        int max_nbVeh, const AlgorithmParameters* ap, char verbose)

    Solution* solve_cvrp_dist_mtx(int n, double* x, double* y, double *dist_mtx, double *serv_time, double *dem,
	                             double vehicleCapacity, double durationLimit, char isDurationConstraint,
	                             int max_nbVeh, const AlgorithmParameters *ap, char verbose)


    void delete_solution(Solution * sol)


class RoutingSolution:
    def __init__(self, cost, time, n_routes, routes):
        self.cost = cost
        self.time = time
        self.n_routes = n_routes
        self.routes = routes

cdef get_solution_py(Solution *sol_c):
    cdef int i, j
    routes_py = []
    for i in range(sol_c.n_routes):
        route_py = {}
        route_py['length'] = sol_c.routes[i].length
        route_py['path'] = [sol_c.routes[i].path[j] for j in range(sol_c.routes[i].length)]
        routes_py.append(route_py)

    sol_py = RoutingSolution(sol_c.cost, sol_c.time, sol_c.n_routes, routes_py)
    return sol_py

# cdef get_algorithm_parameters(
#     int nbGranular, 
#     int mu,
#     int lambda_, 
#     int nbElite, 
#     int nbClose, 
#     double targetFeasible,
#     int seed, 
#     int nbIter, 
#     double timeLimit, 
#     int useSwapStar, 
# ):
#     # Create an instance of AlgorithmParameters C struct and set its values
#     cdef AlgorithmParameters ap

#     ap.nbGranular = nbGranular
#     ap.mu = mu
#     ap.lambda_ = lambda_
#     ap.nbElite = nbElite
#     ap.nbClose = nbClose
#     ap.targetFeasible = targetFeasible
#     ap.seed = seed
#     ap.nbIter = nbIter
#     ap.timeLimit = timeLimit
#     ap.useSwapStar = useSwapStar

#     return ap



def _solve_cvrp_dist_mtx(
    double[:] x,
    double[:] y, 
    double[:] dist_mtx,
    double[:] serv_time, 
    double[:] dem,
    double vehicleCapacity, 
    double durationLimit, 
    char isDurationConstraint,
    int max_nbVeh, 
    int nbGranular, 
    int mu,
    int lambda_, 
    int nbElite, 
    int nbClose, 
    double targetFeasible,
    int seed, 
    int nbIter, 
    double timeLimit, 
    int useSwapStar, 
    char verbose
):

    # Create an instance of AlgorithmParameters C struct and set its values
    # cdef AlgorithmParameters ap
    cdef AlgorithmParameters ap

    ap.nbGranular = nbGranular
    ap.mu = mu
    ap.lambda_ = lambda_
    ap.nbElite = nbElite
    ap.nbClose = nbClose
    ap.targetFeasible = targetFeasible
    ap.seed = seed
    ap.nbIter = nbIter
    ap.timeLimit = timeLimit
    ap.useSwapStar = useSwapStar

    # ap = get_algorithm_parameters(nbGranular, mu, lambda_, nbElite, nbClose, targetFeasible, 
    #                                seed, nbIter, timeLimit, useSwapStar)

    # Convert the Python input arrays to C-compatible arrays
    cdef double *x_c = <double *> &x[0]
    cdef double *y_c = <double *> &y[0]
    cdef double *dist_mtx_c = <double *> &dist_mtx[0]
    cdef double *serv_time_c = <double *> &serv_time[0]
    cdef double *dem_c = <double *> &dem[0]

    # Call the C function
    cdef Solution *sol_c = solve_cvrp_dist_mtx(len(x), x_c, y_c, dist_mtx_c, serv_time_c, dem_c, vehicleCapacity, durationLimit, 
                                      isDurationConstraint, max_nbVeh, &ap, verbose)

    # Convert the C output to Python objects
    sol_py = get_solution_py(sol_c)

    # Free the memory allocated in C
    delete_solution(sol_c)
    
    return sol_py



def _solve_cvrp(
    double[:] x,
    double[:] y, 
    double[:] serv_time, 
    double[:] dem,
    double vehicleCapacity, 
    double durationLimit, 
    char isRoundingInteger, 
    char isDurationConstraint,
    int max_nbVeh, 
    int nbGranular, 
    int mu,
    int lambda_, 
    int nbElite, 
    int nbClose, 
    double targetFeasible,
    int seed, 
    int nbIter, 
    double timeLimit, 
    int useSwapStar, 
    char verbose
):

    # Create an instance of AlgorithmParameters C struct and set its values
    cdef AlgorithmParameters ap

    ap.nbGranular = nbGranular
    ap.mu = mu
    ap.lambda_ = lambda_
    ap.nbElite = nbElite
    ap.nbClose = nbClose
    ap.targetFeasible = targetFeasible
    ap.seed = seed
    ap.nbIter = nbIter
    ap.timeLimit = timeLimit
    ap.useSwapStar = useSwapStar

    # Convert the Python input arrays to C-compatible arrays
    cdef double *x_c = <double *> &x[0]
    cdef double *y_c = <double *> &y[0]
    cdef double *serv_time_c = <double *> &serv_time[0]
    cdef double *dem_c = <double *> &dem[0]

    # Call the C function
    cdef Solution *sol_c = solve_cvrp(len(x), x_c, y_c, serv_time_c, dem_c, vehicleCapacity, durationLimit, 
                                      isRoundingInteger, isDurationConstraint, max_nbVeh, &ap, verbose)

    # Convert the C output to Python objects
    sol_py = get_solution_py(sol_c)

    # Free the memory allocated in C
    delete_solution(sol_c)
    
    return sol_py