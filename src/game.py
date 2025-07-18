import chess
from typing import Literal

from player import Player
from base_game import BaseGame


class Game(BaseGame):
    p1: Player
    p2: Player
    max_retries: int

    @classmethod
    def play(cls, white: Player, black: Player, max_retries: int) -> chess.Outcome:
        game = cls(white, black, max_retries)
        return game.loop_full()

    def __init__(self, white: Player, black: Player, max_retries: int) -> None:
        super().__init__("p1")
        self.p1 = white
        self.p2 = black
        self.max_retries = max_retries

    def get_p1_move(self) -> chess.Move:
        return self.get_player_move("p1")

    def get_p2_move(self) -> chess.Move:
        return self.get_player_move("p2")

    def get_player_move(self, player_number: Literal["p1", "p2"]) -> chess.Move:
        player = self.player(player_number)
        color = self.player_color(player_number)
        (move, _) = player.get_move(self.board, color, self.max_retries)
        return move

    def player(self, player: Literal["p1", "p2"]) -> Player:
        match player:
            case "p1":
                return self.p1
            case "p2":
                return self.p2
