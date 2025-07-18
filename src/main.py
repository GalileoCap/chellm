import argparse

from np_game import NPGame
from sp_game import SPGame
from tp_game import TPGame

M_HELP_BASE = "as is accepted by Langchain's init_chat_model (eg: ollama:llama3.2:8b or openai:o4-mini)."
RETRY_HELP = "Number of retries before stopping execution."

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="chellm", description="Watch LLMs play chess!"
    )
    sub = parser.add_subparsers(dest="player_count", required=True)

    parser.add_argument("-w", choices=["p1", "p2"], default="p1")

    np_parser = sub.add_parser("0", help="No players game (both AI)")
    np_parser.add_argument("-m", help="Model for both players " + M_HELP_BASE)
    np_parser.add_argument(
        "-p1m",
        help="Model for player 1 " + M_HELP_BASE + " Takes precedence over -m.",
    )
    np_parser.add_argument(
        "-p2m",
        help="Model for player 2 " + M_HELP_BASE + " Takes precedence over -m.",
    )
    np_parser.add_argument("--retry", type=int, default=5, help=RETRY_HELP)

    sp_parser = sub.add_parser("1", help="Single player game against AI")
    sp_parser.add_argument(
        "-m",
        required=True,
        help="Model for the AI player "
        + M_HELP_BASE
        + " Used by both players unless specified.",
    )
    sp_parser.add_argument("--retry", type=int, default=5, help=RETRY_HELP)

    tp_parser = sub.add_parser("2", help="Two player game")

    args = parser.parse_args()

    match args.player_count:
        case "0":
            p1_model = args.p1m or args.m
            p2_model = args.p2m or args.m
            if p1_model is None:
                raise ValueError("either -m or -p1m and -p2m are a required")

            game = NPGame(p1_model, p2_model, args.w, args.retry)
        case "1":
            game = SPGame(args.m, args.w, args.retry)
        case "2":
            game = TPGame(args.w)
        case p:
            raise ValueError(f"invalid player count: {p}")

    winner = game.loop_full()
    print(winner)
