#!/usr/bin/env python3
'UI for winning games.'
import tkinter
from tkinter import ttk

import logic

CARD_UI_TO_LOGIC = {
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    '10': 10,
    'J': 11,
    'Q': 12,
    'K': 13,
    'A': 14
}
CARD_LOGIC_TO_UI = {value: key for key, value in CARD_UI_TO_LOGIC.items()}

ROOT = tkinter.Tk()
ROOT.tk.call('tk', 'scaling', 5.0)

class Game:
    def __init__(self):
        self.logic = logic.Game()
        self.frame = ttk.Frame(ROOT)
        self.frame.grid()
        self.table = ttk.Frame(self.frame)
        self.table.grid()
        self.spots = []
        for row in range(3):
            for column in range(3):
                spot = ttk.Combobox(self.table, values=(
                    list(range(2, 11)) + ['J', 'Q', 'K', 'A']
                ), state='readonly')
                spot.grid(column=column, row=row)
                spot.set(CARD_LOGIC_TO_UI[self.logic.table[row * 3 + column]])
                self.spots.append(spot)
        self.button = ttk.Button(self.frame, text="Go!", command=self.calculate)
        self.button.grid(column=4, row=4)

    def calculate(self):
        for spot in self.spots:
            if not spot.get():
                raise ValueError('All cards must be selected.')
        best_spot, is_low = self.logic.get_best_move()
        self.spots[best_spot].set('L' if is_low else 'H')
        self.button.configure(state='disabled')

    def get_best_move(self):
        results = logic.odds(self.table, self.deck.cards)
        scores = [abs(result) for result in results]
        best_spot = scores.index(max(scores))
        return best_spot, results[best_spot] < 0

GAME = Game()
ROOT.mainloop()
