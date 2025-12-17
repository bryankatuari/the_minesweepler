# main.py
import random
from engine.board import Board
from logic_agent.inference import infer


def main():
    w, h = 8, 8
    mine_count = 10
    start = (0, 0)

    all_cells = [(r, c) for r in range(h) for c in range(w)]

    # First click safe: exclude start from mine placement
    candidates = [cell for cell in all_cells if cell != start]
    mines = set(random.sample(candidates, mine_count))

    board = Board(w, h, mines)

    forced_moves = 0
    guesses = 0
    steps = 0

    # First reveal
    if not board.reveal(*start):
        board.visible_print()
        print("\nBOOM — hit a mine on the first click (should not happen). Game over.")
        return

    while True:
        steps += 1
        board.visible_print()
        print()

        if board.game_over:
            print(
                f"Game over. steps={steps}, forced_moves={forced_moves}, guesses={guesses}, flags={len(board.flags)}"
            )
            return

        if board.is_solved():
            print(
                f"Solved! steps={steps}, forced_moves={forced_moves}, guesses={guesses}, flags={len(board.flags)}"
            )
            return

        safe, mines_found, guess_info = infer(board)

        # Apply inferred mines
        for m in mines_found:
            board.flag(*m)

        # Apply inferred safe squares
        made_progress = False
        if safe:
            made_progress = True
            forced_moves += len(safe)
            for s in safe:
                if not board.reveal(*s):
                    board.visible_print()
                    print(
                        "\nBOOM — inferred safe but hit a mine (should not happen). Game over."
                    )
                    return

        # If no forced move, guess smartly (min mine probability)
        if not made_progress:
            unknown_choices = [
                (r, c)
                for r in range(h)
                for c in range(w)
                if not board.is_revealed(r, c) and not board.is_flagged(r, c)
            ]
            if not unknown_choices:
                # Nothing left to do
                if board.is_solved():
                    print(
                        f"Solved! steps={steps}, forced_moves={forced_moves}, guesses={guesses}, flags={len(board.flags)}"
                    )
                else:
                    print("No moves left.")
                return

            if guess_info is not None:
                (gr, gc), p = guess_info
                # if somehow already revealed/flagged, fall back
                if board.is_revealed(gr, gc) or board.is_flagged(gr, gc):
                    gr, gc = random.choice(unknown_choices)
                    p = None
            else:
                gr, gc = random.choice(unknown_choices)
                p = None

            guesses += 1
            ok = board.reveal(gr, gc)
            if not ok:
                board.visible_print()
                if p is None:
                    print(f"\nBOOM — guessed ({gr},{gc}). Game over.")
                else:
                    print(
                        f"\nBOOM — guessed ({gr},{gc}) with mine_prob≈{p:.3f}. Game over."
                    )
                print(
                    f"steps={steps}, forced_moves={forced_moves}, guesses={guesses}, flags={len(board.flags)}"
                )
                return


if __name__ == "__main__":
    main()
