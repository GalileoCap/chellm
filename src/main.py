from np_game import NPGame
from tp_game import TPGame


if __name__ == "__main__":
    model = "llama3.2:3b"
    white = "p1"

    game = NPGame(model, model, white, 5)
    # game = TPGame(white)
    winner = game.loop_full()
    print(winner)
