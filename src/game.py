import chess
from typing import Literal
from langchain_core.runnables import Runnable
from langchain.chat_models import init_chat_model

from ai import get_ai_move
from base_game import BaseGame


class Game(BaseGame):
    p1_llm: Runnable
    p2_llm: Runnable
    max_retries: int

    def __init__(
        self, p1_model: str, p2_model: str, white: Literal["p1", "p2"], max_retries: int
    ) -> None:
        super().__init__(white)
        self.p1_llm = init_chat_model(model=p1_model)
        self.p2_llm = init_chat_model(model=p2_model)
        self.max_retries = max_retries

    def get_p1_move(self) -> chess.Move:
        return self.get_player_move("p1")

    def get_p2_move(self) -> chess.Move:
        return self.get_player_move("p2")

    def get_player_move(self, player: Literal["p1", "p2"]) -> chess.Move:
        llm = self.player_llm(player)
        color = self.player_color(player)
        (move, _) = get_ai_move(llm, color, self.board, self.max_retries)
        return move

    def player_llm(self, player: Literal["p1", "p2"]) -> Runnable:
        match player:
            case "p1":
                return self.p1_llm
            case "p2":
                return self.p2_llm
