from engine.board import Board


def test_board_basic():
    """test 1: random mine generation  and board representation"""
    mines = None
    b = Board(width=10, height=10, num_mines=10, mines=mines)

    print("Full board (* for mines):")
    b.debug_print_full()


def test_reveal_logic():
    """test 2: reveal logic"""
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
    print("Value at (1,1):", v)  # should be -1
    b.visible_print()


if __name__ == "__main__":
    # test_board_basic()
    test_reveal_logic()
