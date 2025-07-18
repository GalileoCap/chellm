import chess
import jinja2
from langchain_core.runnables import Runnable
from langchain_core.messages import HumanMessage, SystemMessage

SYS_PROMPT_PATH: str = "sys_prompt.jinja"


def get_ai_move(llm: Runnable, color: chess.Color, board: chess.Board) -> chess.Move:
    prompt = get_system_prompt().render(
        color=chess.COLOR_NAMES[color],
        board=board,
    )

    reply_msg = llm.invoke([SystemMessage(prompt), HumanMessage("")])
    reply = reply_msg.text().strip().lower()
    if reply == "fold":
        raise NotImplementedError("fold")
    else:
        return board.parse_san(reply)


def get_system_prompt() -> jinja2.Template:
    with open(SYS_PROMPT_PATH, "r") as fin:
        return jinja2.Template(fin.read())
