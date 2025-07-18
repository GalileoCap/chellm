import chess
from typing import Literal
from langchain_core.language_models import BaseChatModel
from langchain_core.runnables import Runnable
from langchain_ollama.chat_models import ChatOllama

from ai import get_ai_move
from base_game import BaseGame


class NPGame(BaseGame):
    p1_llm: BaseChatModel
    p2_llm: BaseChatModel
    max_retries: int

    def __init__(
        self, p1_model: str, p2_model: str, white: Literal["p1", "p2"], max_retries: int
    ) -> None:
        super().__init__(white)
        self.p1_llm = ChatOllama(model=p1_model)
        self.p2_llm = ChatOllama(model=p2_model)
        self.max_retries = max_retries

    def loop_full(self) -> chess.Outcome:
        print(self.board)
        return super().loop_full()

    def loop_step(self) -> None:
        super().loop_step()
        print(self.board)

    def get_p1_move(self) -> chess.Move:
        return self.get_player_move("p1")

    def get_p2_move(self) -> chess.Move:
        return self.get_player_move("p2")

    def get_player_move(self, player: Literal["p1", "p2"]) -> chess.Move:
        print("...")

        llm = self.player_llm(player)
        color = self.player_color(player)
        (move, retries) = get_ai_move(llm, color, self.board, self.max_retries)

        print(f"{move.uci()} in {retries} retries")
        return move

    def player_llm(self, player: Literal["p1", "p2"]) -> Runnable:
        match player:
            case "p1":
                return self.p1_llm
            case "p2":
                return self.p2_llm
