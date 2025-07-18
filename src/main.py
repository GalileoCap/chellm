import argparse

from tournament import Tournament
from player import Player

M_HELP_BASE = "as is accepted by Langchain's init_chat_model (eg: ollama:llama3.2:8b or openai:o4-mini)."
RETRY_HELP = "Number of retries allowed for AI players before stopping execution. Use -1 to allow running for ever."


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
    tournament = Tournament(players, args.retry)
    winner = tournament.loop_full()
    print(winner)
