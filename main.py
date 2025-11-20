from engine.board import Board


def test_board_basic():
    # 3x3 board with a single mine in the center
    mines = [(1, 1)]
    b = Board(width=3, height=3, num_mines=1, mines=mines)

    print("Full board (* for mines):")
    b.debug_print_full()


if __name__ == "__main__":
    test_board_basic()
