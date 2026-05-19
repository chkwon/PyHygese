"""Regression tests for the ctypes memory-safety fixes in hygese.Solver.

- delete_solution must run even when RoutingSolution extraction raises
  (the `try/finally` block in _solve_cvrp / _solve_cvrp_dist_mtx).
- A single Solver must be reusable: each call gets its own ctypes buffers
  and produces a clean result.
"""

import pytest

import hygese.hygese as _hg
from hygese import AlgorithmParameters, Solver


def test_delete_called_on_exception(or_tools_data, quick_ap, monkeypatch):
    solver = Solver(quick_ap, verbose=False)

    delete_calls = []
    original_delete = solver._c_api_delete_sol

    def counting_delete(ptr):
        delete_calls.append(bool(ptr))
        return original_delete(ptr)

    solver._c_api_delete_sol = counting_delete

    def boom(self, sol_ptr):
        raise RuntimeError("simulated extraction failure")

    monkeypatch.setattr(_hg.RoutingSolution, "__init__", boom)

    with pytest.raises(RuntimeError, match="simulated extraction failure"):
        solver.solve_cvrp(or_tools_data)

    assert delete_calls == [True], (
        "delete_solution must be called exactly once with a non-null pointer "
        "when RoutingSolution.__init__ raises"
    )


def test_solver_reuse(or_tools_data):
    ap = AlgorithmParameters(timeLimit=0.5, seed=42)
    solver = Solver(ap, verbose=False)

    costs = [solver.solve_cvrp(or_tools_data).cost for _ in range(3)]

    assert all(c == costs[0] for c in costs), (
        f"Reusing a Solver with seed=42 should give identical costs across "
        f"calls; got {costs}"
    )
    assert costs[0] > 0
