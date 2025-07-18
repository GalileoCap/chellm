import sys
from typing import Literal

import chess

from messages import get_move_error_message


def get_human_move(
    board: chess.Board, *, player: Literal["p1", "p2"] | None = None
) -> chess.Move:
    print(board)

    player_fmt = player if player is not None else ""
    move: chess.Move | None = None
    while move is None:
        raw_move = input(f"{player_fmt}> ")
        if raw_move == "fold":
            raise NotImplementedError("fold")
        else:
            try:
                move = board.parse_san(raw_move)
            except (
                chess.InvalidMoveError,
                chess.IllegalMoveError,
                chess.AmbiguousMoveError,
            ) as err:
                err_msg = get_move_error_message(err)
                print(err_msg, file=sys.stderr)

    return move
