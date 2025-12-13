from typing import List, Set, Tuple
from csp.constraints import Constraint

Coord = Tuple[int, int]  # (row, col)


def infer_safe_and_mines(
    constraints: List[Constraint],
    initially_known_mines: Set[Coord] = None,
    initially_known_safe: Set[Coord] = None,
):
    """
    Deterministic reasoning over Minesweeper constraints.

    constraints: list of Constraint, where each has:
      - variables: list[(r,c)]
      - required_sum: number of mines among those variables

    initially_known_mines / initially_known_safe:
      optional sets of (r,c) you already know.

    Returns:
      (safe_cells, mine_cells) as sets of (r,c).
    """
    known_mines: Set[Coord] = set(initially_known_mines or set())
    known_safe: Set[Coord] = set(initially_known_safe or set())

    changed = True
    while changed:
        changed = False

        for c in constraints:
            vars_set = set(c.variables)

            unknown = vars_set - known_mines - known_safe
            if not unknown:
                continue

            # mines already assigned in this constraint
            mines_here = vars_set & known_mines
            remaining_mines = c.required_sum - len(mines_here)

            # Rule 1: no remaining mines -> unknown are safe
            if remaining_mines == 0:
                new_safe = unknown - known_safe
                if new_safe:
                    known_safe |= new_safe
                    changed = True

            # Rule 2: all unknown must be mines
            elif remaining_mines == len(unknown):
                new_mines = unknown - known_mines
                if new_mines:
                    known_mines |= new_mines
                    changed = True

    return known_safe, known_mines
