import argparse
import random

from game import Game
from player import Player

M_HELP_BASE = "as is accepted by Langchain's init_chat_model (eg: ollama:llama3.2:8b or openai:o4-mini)."
RETRY_HELP = "Number of retries allowed for AI players before stopping execution. Use -1 to allow running for ever."


def draw_players(
    players: list[Player],
) -> list[tuple[Player, Player]]:
    pairs = []
    while len(players) >= 2:
        (p1, p2) = random.sample(players, 2)
        pairs.append((p1, p2))
        players.remove(p1)
        players.remove(p2)
    return pairs


def run_tournament(players: list[Player]) -> Player:
    assert len(players) != 0, "at least one player is required"

    while len(players) > 1:
        pairs = draw_players(players)
        for p1, p2 in pairs:
            game = Game(p1, p2, args.retry)
            outcome = game.loop_full()
            match outcome:
                case "white" | "black-failed":
                    players.append(p1)
                case "black" | "white-failed":
                    players.append(p2)
                case "draw":
                    players.append(p1)
                    players.append(p2)
    return players[0]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="chellm", description="Watch LLMs play chess!"
    )

    parser.add_argument(
        "models",
        nargs="+",
        help="Comma separated list of models used by players " + M_HELP_BASE,
    )
    parser.add_argument("--retry", type=int, required=True, help=RETRY_HELP)

    args = parser.parse_args()

    players = list(map(Player, args.models))
    winner = run_tournament(players)
    print(winner)
