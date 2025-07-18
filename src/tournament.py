import random

from game import Game
from player import Player


class Tournament:
    players: list[Player]
    max_retries: int

    def __init__(self, players: list[Player], max_retries: int) -> None:
        assert len(players) != 0, "at least one player is required"

        self.players = players
        self.max_retries = max_retries

    def loop_full(self) -> Player:
        while len(self.players) > 1:
            self.loop_step()
        return self.players[0]

    def loop_step(self):
        pairs = self.draw_players()
        for p1, p2 in pairs:
            pls = self.play_pair(p1, p2)
            self.players.extend(pls)

    def play_pair(self, p1: Player, p2: Player) -> list[Player]:
        game = Game(p1, p2, self.max_retries)
        outcome = game.loop_full()
        match outcome:
            case "white" | "black-failed":
                return [p1]
            case "black" | "white-failed":
                return [p2]
            case "draw":
                return [p1, p2]

    def draw_players(self) -> list[tuple[Player, Player]]:
        pairs = []
        while len(self.players) >= 2:
            (p1, p2) = random.sample(self.players, 2)
            pairs.append((p1, p2))
            self.players.remove(p1)
            self.players.remove(p2)
        return pairs
