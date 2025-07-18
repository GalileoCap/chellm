from np_game import NPGame


if __name__ == "__main__":
    model = "llama3.2:3b"
    white = "p1"

    game = NPGame(model, model, white)
    winner = game.loop_full()
    print(winner)
