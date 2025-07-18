import abc
import chess
from typing import Literal, cast


class BaseGame(abc.ABC):
    board: chess.Board
    white: Literal["p1", "p2"]

    def __init__(self, white: Literal["p1", "p2"]) -> None:
        self.board = chess.Board()
        self.white = white

    def loop_full(self) -> chess.Outcome:
        claim_draw = False
        while not self.board.is_game_over(claim_draw=claim_draw):
            self.loop_step()
        outcome = self.board.outcome(claim_draw=claim_draw)
        return cast(chess.Outcome, outcome)

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
        match self.white:
            case "p1":
                return self.get_p1_move()
            case "p2":
                return self.get_p2_move()

    def get_black_move(self) -> chess.Move:
        match self.white:
            case "p1":
                return self.get_p2_move()
            case "p2":
                return self.get_p1_move()

    @abc.abstractmethod
    def get_p1_move(self) -> chess.Move:
        pass

    @abc.abstractmethod
    def get_p2_move(self) -> chess.Move:
        pass

    def player_color(self, player: Literal["p1", "p2"]) -> chess.Color:
        match player:
            case "p1":
                return self.p1_color
            case "p2":
                return self.p2_color

    @property
    def p1_color(self) -> chess.Color:
        return chess.WHITE if self.white == "p1" else chess.BLACK

    @property
    def p2_color(self) -> chess.Color:
        return chess.WHITE if self.white == "p2" else chess.BLACK
