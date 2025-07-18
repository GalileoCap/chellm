import chess
from typing import Literal

from base_game import BaseGame
from human import get_human_move


class TPGame(BaseGame):
    def __init__(self, white: Literal["p1", "p2"]) -> None:
        super().__init__(white)

    def get_p1_move(self) -> chess.Move:
        return self.get_player_move("p1")

    def get_p2_move(self) -> chess.Move:
        return self.get_player_move("p2")

    def get_player_move(self, player: Literal["p1", "p2"]) -> chess.Move:
        return get_human_move(self.board, player=player)
