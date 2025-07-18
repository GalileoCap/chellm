import argparse

from game import Game, Player

M_HELP_BASE = "as is accepted by Langchain's init_chat_model (eg: ollama:llama3.2:8b or openai:o4-mini)."
RETRY_HELP = "Number of retries allowed for AI players before stopping execution. Use -1 to allow running for ever."

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="chellm", description="Watch LLMs play chess!"
    )

    parser.add_argument("-m", help="Model for both players " + M_HELP_BASE)
    parser.add_argument(
        "-p1m",
        help="Model for player 1 " + M_HELP_BASE + " Takes precedence over -m.",
    )
    parser.add_argument(
        "-p2m",
        help="Model for player 2 " + M_HELP_BASE + " Takes precedence over -m.",
    )
    parser.add_argument("--retry", type=int, required=True, help=RETRY_HELP)

    args = parser.parse_args()

    p1_model = args.p1m or args.m
    p2_model = args.p2m or args.m
    if p1_model is None:
        raise ValueError("either -m or -p1m and -p2m are a required")

    p1 = Player("p1", p1_model)
    p2 = Player("p2", p1_model)

    game = Game(p1, p2, args.retry)
    winner = game.loop_full()
    print(winner)
