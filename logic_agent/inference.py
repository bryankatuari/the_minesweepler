# logic_agent/inference.py
from csp.model import build_constraints_from_board


def _select_unassigned_var_mrv(variables, domains, assignment, constraints):
    """
    MRV: choose unassigned var with smallest domain.
    Tie-break: most constraining (appears in most constraints).
    """
    unassigned = [v for v in variables if v not in assignment]

    def key(v):
        dom_size = len(domains[v])
        degree = sum(1 for c in constraints if v in c.variables)
        return (dom_size, -degree)

    return min(unassigned, key=key)


def _forward_check(domains, constraints, assignment):
    """
    Basic filtering: if any constraint is already impossible under current assignment, fail.
    (Domains are {0,1}, so we keep it simple & fast.)
    """
    for c in constraints:
        if not c.is_satisfied(assignment):
            return False
    return True


def _backtrack_all_solutions(
    variables, constraints, domains, assignment, solutions, max_solutions=50000
):
    """
    Enumerate satisfying assignments over the frontier variables.
    cap with max_solutions to avoid exploding on very large frontiers.
    """
    if len(solutions) >= max_solutions:
        return

    if len(assignment) == len(variables):
        solutions.append(dict(assignment))
        return

    var = _select_unassigned_var_mrv(variables, domains, assignment, constraints)

    # LCV: try value that rules out fewer options — here approximate by trying 0 then 1
    for val in (0, 1):
        assignment[var] = val
        if _forward_check(domains, constraints, assignment):
            _backtrack_all_solutions(
                variables,
                constraints,
                domains,
                assignment,
                solutions,
                max_solutions=max_solutions,
            )
        del assignment[var]

        if len(solutions) >= max_solutions:
            return


def infer(board, max_solutions=50000):
    """
    Returns:
      safe_set: cells proven safe (0 in all solutions)
      mine_set: cells proven mines (1 in all solutions)
      guess_info: ((r,c), mine_probability) for best guess, or None
    """
    constraints = build_constraints_from_board(board)

    # Frontier variables = all unknown cells that appear in any constraint
    variables = sorted({v for c in constraints for v in c.variables})

    # If nothing to reason about, no inference
    if not variables:
        return set(), set(), None

    # Domains: boolean
    domains = {v: {0, 1} for v in variables}

    solutions = []
    _backtrack_all_solutions(
        variables, constraints, domains, {}, solutions, max_solutions=max_solutions
    )

    if not solutions:
        # Inconsistent state (usually from a bad guess earlier) or over-flagging.
        return set(), set(), None

    safe = set()
    mines = set()

    # forced classification
    for v in variables:
        vals = {sol[v] for sol in solutions}
        if vals == {0}:
            safe.add(v)
        elif vals == {1}:
            mines.add(v)

    # If we have forced moves, don't bother guessing
    if safe or mines:
        return safe, mines, None

    # Otherwise compute mine probabilities for guessing
    total = len(solutions)
    mine_counts = {v: 0 for v in variables}
    for sol in solutions:
        for v in variables:
            mine_counts[v] += sol[v]

    probs = {v: mine_counts[v] / total for v in variables}

    # Pick minimum mine probability among currently unknown/unflagged cells
    candidates = [
        v
        for v in variables
        if (not board.is_revealed(*v)) and (not board.is_flagged(*v))
    ]
    if not candidates:
        return set(), set(), None

    best = min(candidates, key=lambda v: probs[v])
    return set(), set(), (best, probs[best])
