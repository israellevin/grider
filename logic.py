#!/usr/bin/env python3
'Solitaire card game.'
import random


def make_deck():
    return list(range(2, 15)) * 4


def deal(deck):
    return deck.pop(random.randint(0, len(deck) - 1))


def make_table(deck):
    return [deal(deck) for _ in range(9)]


def play_round(table, deck, index, is_high):
    new_card = deal(deck)
    if table[index] - new_card > 0 != is_high:
        table.pop(index)
        return False
    table[index] = new_card
    return True


def odds(table, deck):
    results = []
    for spot in table:
        lows = 0
        for card in deck:
            if spot - card > 0:
                lows += 1
        results.append(lows - (len(deck) / 2))
    return results


def play_game():
    deck = make_deck()
    table = make_table(deck)
    while len(table) > 0 and len(deck) > 0:
        results = odds(table, deck)
        scores = [abs(result) for result in results]
        best_spot = scores.index(max(scores))
    return len(deck)


class Deck:
    def __init__(self):
        self.cards = make_deck()

    def deal(self):
        return self.cards.pop(random.randint(0, len(self.cards) - 1))

    def draw(self, card):
        return self.cards.pop(self.cards.index(card))

    def draw_many(self, cards):
        for card in cards:
            self.draw(card)


class Game:
    def __init__(self, table=None):
        self.deck = Deck()
        self.table = table if table else make_table(self.deck.cards)
        self.deck.draw_many(self.table)

    def get_best_move(self):
        results = odds(self.table, self.deck.cards)
        scores = [abs(result) for result in results]
        best_spot = scores.index(max(scores))
        return best_spot, results[best_spot] > 0
