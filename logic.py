#!/usr/bin/env python3
'Solitaire card game.'
import random
import sys


class Game:

    def __init__(self, table=None):
        self.deck = list(range(2, 15)) * 4
        self.table = self.draw_many(table) if table else [self.draw() for _ in range(9)]

    def draw(self, card=None):
        if not card:
            card = random.choice(self.deck)
        return self.deck.pop(self.deck.index(card))

    def draw_many(self, cards):
        return [self.draw(card) for card in cards]

    def recommend(self):
        results = []
        for spot in self.table:
            lows = 0
            for card in self.deck:
                if spot - card > 0:
                    lows += 1
            results.append(lows - (len(self.deck) / 2))
        scores = [abs(result) for result in results]
        best_spot = scores.index(max(scores))
        return best_spot, results[best_spot] > 0

    def play_round(self, index, is_high, new_card=None):
        new_card = self.draw(new_card)
        if (self.table[index] > new_card) != is_high:
            self.table.pop(index)
            return False
        self.table[index] = new_card
        return True


def play_game():
    game = Game()
    while len(game.table) > 0 and len(game.deck) > 0:
        game.play_round(*game.recommend())
    return len(game.deck)


if __name__ == '__main__':
    num_games = int(sys.argv[1]) if len(sys.argv) > 1 else 10**4
    num_wins = sum([1 if play_game() == 0 else 0 for _ in range(num_games)])
    print(f'{num_wins} wins out of {num_games} games.')
