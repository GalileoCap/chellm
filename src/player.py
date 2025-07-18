from typing import cast

import chess
import jinja2
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, AnyMessage, HumanMessage, SystemMessage
from langchain.chat_models import init_chat_model

SYS_PROMPT: jinja2.Template | None = None
SYS_PROMPT_PATH: str = "sys_prompt.jinja"


class Player:
    id: str
    model: str
    llm: BaseChatModel

    def __init__(self, id: str, model: str) -> None:
        self.id = id
        self.model = model
        self.llm = init_chat_model(model=model)

    def get_move(
        self, board: chess.Board, color: chess.Color, max_retries: int
    ) -> tuple[chess.Move, int]:
        prompt = get_system_prompt().render(
            color=chess.COLOR_NAMES[color],
            board=board,
        )

        history: list[AnyMessage] = [SystemMessage(prompt), HumanMessage("Your turn")]
        retries = 0
        move: chess.Move | None = None
        while move is None and (retries == 0 or should_retry(retries, max_retries)):
            reply_msg = self.llm.invoke(history)
            reply_msg = cast(AnyMessage, reply_msg)
            history.append(reply_msg)
            retries += 1

            reply = reply_msg.text().strip().lower()
            if reply == "fold":
                raise NotImplementedError("fold")
            else:
                try:
                    move = board.parse_san(reply)
                except (
                    chess.InvalidMoveError,
                    chess.IllegalMoveError,
                    chess.AmbiguousMoveError,
                ) as err:
                    err_msg = get_move_error_message(err)
                    history.append(HumanMessage(err_msg))

        if move is None:
            ai_messages = filter(lambda m: isinstance(m, AIMessage), history)
            history_fmt = [m.text().strip().lower() for m in ai_messages]
            raise RuntimeError(
                f"failed to produce a valid move in {retries} retries, tries: {history_fmt}"
            )
        return (move, retries)


def should_retry(retries: int, max_retries: int) -> bool:
    return (
        max_retries == -1  # Infinite retries
        or retries == 0  # First trye
        or retries < max_retries
        # or input("retry? (Y/n)").strip().lower() == "n")
    )


def get_system_prompt() -> jinja2.Template:
    global SYS_PROMPT

    if SYS_PROMPT is None:
        with open(SYS_PROMPT_PATH, "r") as fin:
            SYS_PROMPT = jinja2.Template(fin.read())
    return cast(jinja2.Template, SYS_PROMPT)


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
