from engine.board import Board
from csp.model import build_constraints_from_board
from logic_agent.inference import infer_safe_and_mines


def test_board_basic():
    """Test random and fixed mine generation for board representation"""
    mines = None
    b = Board(width=10, height=10, num_mines=10, mines=mines)

    print("Full board (* for mines):")
    b.debug_print_full()


def test_reveal_logic():
    """Test reveal logic"""
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
    """Test constraint logic"""
    mines = [(1, 1)]
    b = Board(width=3, height=3, num_mines=1, mines=mines)

    # reveal some cells to get clues
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


def test_inference_simple_mine():
    print("=== Test: simple mine inference ===")
    mines = [(0, 1)]
    b = Board(width=2, height=2, num_mines=1, mines=mines)

    # Reveal (0,0): neighbors = [(0,1), (1,0), (1,1)]
    # Only one mine total; but other neighbors might be covered
    b.reveal(0, 0)

    print("Visible board:")
    b.visible_print()
    print()

    constraints = build_constraints_from_board(b)
    print("Constraints:", constraints)

    safe, mines_deduced = infer_safe_and_mines(constraints)

    print("Inferred safe cells:", safe)
    print("Inferred mine cells:", mines_deduced)
    print()


def demo():
    print("=== Deterministic Inference Test ===\n")

    # 3x3 board with a single mine at (0,1)
    mines = {(0, 1)}
    b = Board(width=3, height=3, num_mines=len(mines), mines=mines)

    print("FULL INTERNAL BOARD (for debugging / presentation):")
    b.debug_print_full()
    print("\n")

    # Reveal a pattern that forces deduction:
    # - Reveal (0,0), (1,0), (1,1)
    #   For cell (0,0): clue = 1, and its only covered neighbor will be (0,1),
    #   so the constraint is: sum([(0,1)]) = 1  -> (0,1) must be a mine.
    for r, c in [(0, 0), (1, 0), (1, 1)]:
        b.reveal(r, c)

    print("VISIBLE BOARD BEFORE INFERENCE:")
    b.visible_print()
    print("\n")

    # Build constraints from the partially revealed state
    constraints = build_constraints_from_board(b)
    print("GENERATED CONSTRAINTS:")
    for c in constraints:
        print("  ", c)
    print()

    # Run deterministic inference
    safe, mines_deduced = infer_safe_and_mines(constraints)

    print("INFERRED SAFE CELLS:")
    print(" ", safe, "\n")

    print("INFERRED MINES:")
    print(" ", mines_deduced, "\n")

    # Apply inference: flag mines, reveal safe cells
    for cell in mines_deduced:
        b.flags.add(cell)
    for r, c in safe:
        b.reveal(r, c)

    print("VISIBLE BOARD AFTER INFERENCE:")
    b.visible_print()
    print("\n")


if __name__ == "__main__":
    demo()
