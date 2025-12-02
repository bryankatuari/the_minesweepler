# csp/model.py
from .constraints import Constraint


def build_constraints_from_board(board):
    """
    Look at each revealed numbered cell on the board and generate constraints:
    sum(unknown_neighbors) = clue - flagged_neighbors
    """
    constraints = []

    for r in range(board.h):
        for c in range(board.w):
            # Only use revealed, non-mine cells with numbers
            if board.covered[r][c]:
                continue
            if (r, c) in board.mines:
                continue

            clue = board.grid[r][c]
            if clue == 0:
                continue  # no mines around, no info

            neighbors = list(board.get_neighbors(r, c))
            unknowns = [
                pos
                for pos in neighbors
                if board.covered[pos[0]][pos[1]] and pos not in board.flags
            ]
            flagged = [pos for pos in neighbors if pos in board.flags]

            req = clue - len(flagged)
            if unknowns and req >= 0:
                constraints.append(Constraint(unknowns, req))

    return constraints
