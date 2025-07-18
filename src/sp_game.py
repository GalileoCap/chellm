import chess
from typing import Literal
from langchain_core.language_models import BaseChatModel
from langchain_ollama.chat_models import ChatOllama

from ai import get_ai_move
from base_game import BaseGame


class SPGame(BaseGame):
    llm: BaseChatModel

    def __init__(self, model: str, white: Literal["p1", "p2"]) -> None:
        super().__init__(white)
        self.llm = ChatOllama(model=model)

    def get_p1_move(self) -> chess.Move:
        print(self.board)
        msg = input("> ")
        return self.board.parse_san(msg)

    def get_p2_move(self) -> chess.Move:
        print("...")
        move = get_ai_move(self.llm, self.p2_color, self.board)
        print(move.uci())
        return move
