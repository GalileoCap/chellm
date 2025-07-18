import chess
from typing import Literal
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_ollama.chat_models import ChatOllama

from base_game import BaseGame
from utils import get_system_prompt


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

        prompt = get_system_prompt().render(
            color=chess.COLOR_NAMES[self.p2_color],
            board=self.board,
        )

        reply_msg = self.llm.invoke([SystemMessage(prompt), HumanMessage("")])
        reply = reply_msg.text().strip().lower()
        if reply == "fold":
            raise NotImplementedError("fold")
        else:
            move = self.board.parse_san(reply)
            print(move.uci())
            return move
