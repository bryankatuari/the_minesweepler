# engine/board.py


class Board:
    def __init__(self, w, h, mines):
        self.w = w
        self.h = h
        self.mines = set(mines)
        self.flags = set()
        self.revealed = set()
        self.game_over = False

        # -1 for mines, otherwise clue number
        self.grid = [[0] * w for _ in range(h)]
        for r, c in self.mines:
            self.grid[r][c] = -1

        for r in range(h):
            for c in range(w):
                if self.grid[r][c] == -1:
                    continue
                self.grid[r][c] = sum(
                    (nr, nc) in self.mines for nr, nc in self.neighbors(r, c)
                )

    def neighbors(self, r, c):
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.h and 0 <= nc < self.w:
                    yield nr, nc

    def is_revealed(self, r, c):
        return (r, c) in self.revealed

    def is_flagged(self, r, c):
        return (r, c) in self.flags

    def flag(self, r, c):
        if (r, c) not in self.revealed:
            self.flags.add((r, c))

    def reveal(self, r, c):
        """
        Returns True if safe, False if hit a mine.
        Performs flood fill on zeros.
        """
        if self.game_over:
            return False

        if (r, c) in self.flags or (r, c) in self.revealed:
            return True

        self.revealed.add((r, c))

        if (r, c) in self.mines:
            self.game_over = True
            return False

        if self.grid[r][c] == 0:
            for nr, nc in self.neighbors(r, c):
                if (nr, nc) not in self.revealed and (nr, nc) not in self.flags:
                    ok = self.reveal(nr, nc)
                    if not ok:
                        return False

        return True

    def is_solved(self):
        # Solved when all non-mine squares are revealed
        return len(self.revealed) == self.w * self.h - len(self.mines)

    def visible_print(self):
        """
        Prints what the player/agent should see.
        Mines are only shown as '*' after game over.
        """
        for r in range(self.h):
            row = ""
            for c in range(self.w):
                cell = (r, c)
                if cell in self.flags:
                    row += " F "
                elif cell not in self.revealed:
                    if self.game_over and cell in self.mines:
                        row += " * "
                    else:
                        row += " ? "
                else:
                    # revealed
                    if cell in self.mines:
                        row += " * "  # only possible right at death
                    else:
                        row += f" {self.grid[r][c]} "
            print(row)
