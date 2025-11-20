import random


class Board:
    """
    Minesweeper board.
    grid[r][c] = -1 for mine, 0-8 for number of neighboring mines
    covered[r][c] = True if cell is still hidden
    """

    def __init__(self, width, height, num_mines, mines=None):
        self.w = width
        self.h = height
        self.num_mines = num_mines
        self.mines = set()
        self.grid = [[0 for _ in range(width)] for _ in range(height)]
        self.covered = [[True for _ in range(width)] for _ in range(height)]
        self.flags = set()

        if mines is not None:
            # deterministic layout for testing
            assert len(mines) == num_mines, "mines list must match num_mines"
            self.mines = set(mines)
        else:
            self._place_mines_random()

        self._compute_numbers()

    def _place_mines_random(self):
        all_cells = [(r, c) for r in range(self.h) for c in range(self.w)]
        for r, c in random.sample(all_cells, self.num_mines):
            self.mines.add((r, c))

    def _compute_numbers(self):
        for r in range(self.h):
            for c in range(self.w):
                if (r, c) in self.mines:
                    self.grid[r][c] = -1
                else:
                    self.grid[r][c] = sum(
                        (nr, nc) in self.mines for (nr, nc) in self.get_neighbors(r, c)
                    )

    def get_neighbors(self, r, c):
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.h and 0 <= nc < self.w:
                    yield (nr, nc)

    def reveal(self, r, c):
        """
        Reveal a cell.
        Returns:
          -1 if mine,
          0-8 for number of neighboring mines otherwise.
        Auto-expands neighbors if result is 0.
        """
        if not self.covered[r][c]:
            # already revealed
            return self.grid[r][c]

        self.covered[r][c] = False

        if (r, c) in self.mines:
            return -1

        value = self.grid[r][c]
        if value == 0:
            self._flood_fill_from(r, c)
        return value

    def _flood_fill_from(self, r, c):
        """Reveal neighbors recursively for zero-valued cells."""
        stack = [(r, c)]
        while stack:
            cr, cc = stack.pop()
            for nr, nc in self.get_neighbors(cr, cc):
                if self.covered[nr][nc] and (nr, nc) not in self.mines:
                    self.covered[nr][nc] = False
                    if self.grid[nr][nc] == 0:
                        stack.append((nr, nc))

    def is_mine(self, r, c):
        return (r, c) in self.mines

    def all_safe_revealed(self):
        """Check win condition."""
        for r in range(self.h):
            for c in range(self.w):
                if (r, c) not in self.mines and self.covered[r][c]:
                    return False
        return True

    def visible_print(self):
        """Print what a player / agent can see (covered, flags, numbers)."""
        for r in range(self.h):
            row = []
            for c in range(self.w):
                if (r, c) in self.flags:
                    row.append("F")
                elif self.covered[r][c]:
                    row.append("#")  # hidden
                else:
                    if (r, c) in self.mines:
                        row.append("*")
                    else:
                        row.append(str(self.grid[r][c]))
            print(" ".join(row))

    def debug_print_full(self):
        """Print full board (including mines) for debugging."""
        for r in range(self.h):
            row = []
            for c in range(self.w):
                if (r, c) in self.mines:
                    row.append("*")
                else:
                    row.append(str(self.grid[r][c]))
            print(" ".join(row))
