from typing import Literal, cast

import chess

from player import Player
from utils import FailedToMove

Outcome = Literal["white", "black", "draw", "white-failed", "black-failed"]


class Game:
    board: chess.Board
    white: Player
    black: Player
    max_retries: int

    @classmethod
    def play(cls, white: Player, black: Player, max_retries: int) -> Outcome:
        game = cls(white, black, max_retries)
        return game.loop_full()

    def __init__(self, white: Player, black: Player, max_retries: int) -> None:
        self.board = chess.Board()
        self.white = white
        self.black = black
        self.max_retries = max_retries

    def loop_full(self) -> Outcome:
        claim_draw = False
        while not self.board.is_game_over(claim_draw=claim_draw):
            try:
                self.loop_step()
            except FailedToMove:
                match self.board.turn:
                    case chess.WHITE:
                        return "white-failed"
                    case chess.BLACK:
                        return "white-failed"
                    case t:
                        raise RuntimeError(f"invalid board turn: {t}")

        outcome = self.board.outcome(claim_draw=claim_draw)
        outcome = cast(chess.Outcome, outcome)
        match outcome.winner:
            case chess.WHITE:
                return "white"
            case chess.BLACK:
                return "black"
            case None:
                return "draw"
            case w:
                raise RuntimeError(f"invalid winner: {w}")

    def loop_step(self) -> None:
        match self.board.turn:
            case chess.WHITE:
                move = self.get_white_move()
            case chess.BLACK:
                move = self.get_black_move()
            case t:
                raise RuntimeError(f"invalid board turn: {t}")
        self.board.push(move)

    def get_white_move(self) -> chess.Move:
        return self.get_player_move(self.white, chess.WHITE)

    def get_black_move(self) -> chess.Move:
        return self.get_player_move(self.black, chess.BLACK)

    def get_player_move(self, player: Player, color: chess.Color) -> chess.Move:
        (move, _) = player.get_move(self.board, color, self.max_retries)
        return move
