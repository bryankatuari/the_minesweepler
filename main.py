from engine.board import Board
from csp.model import build_constraints_from_board


def test_board_basic():
    """Test 1: Random and fixed mine generation  and board representation"""
    mines = None
    b = Board(width=10, height=10, num_mines=10, mines=mines)

    print("Full board (* for mines):")
    b.debug_print_full()


def test_reveal_logic():
    """Test 2: Reveal logic"""
    mines = [(2, 2), (3, 3)]
    b = Board(width=5, height=5, num_mines=2, mines=mines)

    print("Initial visible board:")
    b.visible_print()
    print()

    print("Reveal (0, 0)…")
    v = b.reveal(0, 0)
    print("Value at (0,0):", v)
    b.visible_print()
    print("Win?", b.all_safe_revealed())
    print()

    print("Reveal a mine at (1, 1)…")
    v = b.reveal(1, 1)
    print("Value at (1,1):", v)
    b.visible_print()


def test_constraints():
    mines = [(1, 1)]
    b = Board(width=3, height=3, num_mines=1, mines=mines)

    # Reveal some cells to get clues
    b.reveal(0, 0)  # 1
    b.reveal(0, 1)  # 1
    b.reveal(1, 0)  # 1

    print("Visible board:")
    b.visible_print()
    print()

    constraints = build_constraints_from_board(b)
    print("Constraints:")
    for c in constraints:
        print(c)


if __name__ == "__main__":
    test_constraints()
