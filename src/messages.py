import chess


def get_move_error_message(
    err: chess.InvalidMoveError | chess.IllegalMoveError | chess.AmbiguousMoveError,
) -> str:
    match type(err):
        case chess.InvalidMoveError:
            return "That is not a valid long SAN move"
        case chess.IllegalMoveError:
            return "That is an illegal move"
        case chess.AmbiguousMoveError:
            return "That move is ambiguous, specify the start and end positions"
        case _:
            raise ValueError(f"invalid error: {err}")
