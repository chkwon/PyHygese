"""Input-variant and validation tests for hygese.Solver.solve_cvrp.

Variant tests pin down the dtype / contiguity branches of np.ascontiguousarray
in _solve_cvrp and _solve_cvrp_dist_mtx. Validation tests pin down the
explicit ValueError / assertion guards in solve_cvrp.
"""

import numpy as np
import pytest

from hygese import AlgorithmParameters, Solver


# --- helpers ---------------------------------------------------------------


def _tiny_coord_data():
    """A tiny coord-based CVRP instance used by variant tests that need coords."""
    return {
        "x_coordinates": [10.0, 20.0, 30.0, 40.0, 50.0],
        "y_coordinates": [50.0, 40.0, 30.0, 20.0, 10.0],
        "demands": [0, 2, 3, 1, 2],
        "vehicle_capacity": 5,
        "depot": 0,
    }


# --- dtype / contiguity correctness ----------------------------------------


def test_float32_inputs_match_float64(quick_ap):
    solver = Solver(quick_ap, verbose=False)

    base = _tiny_coord_data()
    f64 = {
        **base,
        "x_coordinates": np.asarray(base["x_coordinates"], dtype=np.float64),
        "y_coordinates": np.asarray(base["y_coordinates"], dtype=np.float64),
        "demands": np.asarray(base["demands"], dtype=np.float64),
    }
    f32 = {
        **base,
        "x_coordinates": np.asarray(base["x_coordinates"], dtype=np.float32),
        "y_coordinates": np.asarray(base["y_coordinates"], dtype=np.float32),
        "demands": np.asarray(base["demands"], dtype=np.float32),
    }

    cost_f64 = solver.solve_cvrp(f64).cost
    cost_f32 = solver.solve_cvrp(f32).cost
    assert cost_f64 == cost_f32


def test_non_contiguous_distance_matrix(or_tools_data, quick_ap):
    """A non-C-contiguous (F-contiguous transpose of a symmetric matrix) view
    must produce the same cost as the contiguous original — ascontiguousarray
    is responsible for the layout copy.
    """
    solver = Solver(quick_ap, verbose=False)

    base = or_tools_data
    cost_contig = solver.solve_cvrp(base).cost

    m = np.asarray(base["distance_matrix"], dtype=np.float64)
    assert np.array_equal(m, m.T), "OR-Tools matrix should be symmetric"
    non_contig = m.T  # F-contiguous view, same numerical content
    assert not non_contig.flags["C_CONTIGUOUS"]

    variant = {**base, "distance_matrix": non_contig}
    cost_view = solver.solve_cvrp(variant).cost

    assert cost_contig == cost_view


def test_int_demands_accepted(quick_ap):
    """np.int64 demands must round-trip through ascontiguousarray(float64)."""
    solver = Solver(quick_ap, verbose=False)

    data = _tiny_coord_data()
    data["demands"] = np.array(data["demands"], dtype=np.int64)

    result = solver.solve_cvrp(data)
    assert result.cost > 0
    assert result.n_routes >= 1


def test_list_coordinates_accepted(quick_ap):
    """Plain Python list coordinates must work through asarray -> ascontiguousarray."""
    solver = Solver(quick_ap, verbose=False)

    result = solver.solve_cvrp(_tiny_coord_data())
    assert result.cost > 0
    assert result.n_routes >= 1


def test_nbveh_alias_is_supported(monkeypatch, quick_ap):
    solver = Solver(quick_ap, verbose=False)
    seen = {}

    def fake_solve_cvrp(
        x_coords,
        y_coords,
        service_times,
        demand,
        vehicle_capacity,
        duration_limit,
        is_rounding_integer,
        is_duration_constraint,
        maximum_number_of_vehicles,
        algorithm_parameters,
        verbose,
    ):
        seen["maximum_number_of_vehicles"] = maximum_number_of_vehicles
        return object()

    monkeypatch.setattr(solver, "_solve_cvrp", fake_solve_cvrp)

    data = _tiny_coord_data()
    data["nbVeh"] = 7

    solver.solve_cvrp(data)
    assert seen["maximum_number_of_vehicles"] == 7


# --- input validation ------------------------------------------------------


def test_invalid_depot_raises_value_error(or_tools_data, quick_ap):
    solver = Solver(quick_ap, verbose=False)
    or_tools_data["depot"] = 1
    with pytest.raises(ValueError, match="depot location must be 0"):
        solver.solve_cvrp(or_tools_data)


def test_mismatched_lengths_raises_assertion(or_tools_data, quick_ap):
    """Coords explicitly shorter than demands must trip the length assertion."""
    solver = Solver(quick_ap, verbose=False)
    or_tools_data["x_coordinates"] = [0.0, 1.0]
    or_tools_data["y_coordinates"] = [0.0, 1.0]
    with pytest.raises(AssertionError):
        solver.solve_cvrp(or_tools_data)


def test_negative_demand_raises_assertion(or_tools_data, quick_ap):
    solver = Solver(quick_ap, verbose=False)
    or_tools_data["demands"][1] = -1
    with pytest.raises(AssertionError):
        solver.solve_cvrp(or_tools_data)
