# csp/model.py
from csp.constraints import SumConstraint


def build_constraints_from_board(board):
    """
    For each revealed clue cell with value k:
      Let U = unknown neighbors (not revealed, not flagged)
      Let F = number of flagged neighbors
      Add constraint: sum(U) = k - F
    """
    constraints = []

    for r in range(board.h):
        for c in range(board.w):
            if not board.is_revealed(r, c):
                continue

            clue = board.grid[r][c]
            if clue < 0:
                continue  # shouldn't happen mid-game, but safe guard

            unknown = []
            flagged = 0

            for nr, nc in board.neighbors(r, c):
                if board.is_flagged(nr, nc):
                    flagged += 1
                elif not board.is_revealed(nr, nc):
                    unknown.append((nr, nc))

            if unknown:
                total = clue - flagged
                # If something is inconsistent (e.g., too many flags), the CSP will return no solutions
                constraints.append(SumConstraint(unknown, total))

    return constraints
