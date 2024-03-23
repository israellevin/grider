#!/usr/bin/env python3
'UI for winning games.'
import tkinter
from tkinter import ttk

import logic

ROOT = tkinter.Tk()
ROOT.tk.call('tk', 'scaling', 5.0)

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


class Game:
    def __init__(self):
        self.frame = ttk.Frame(ROOT)
        self.frame.grid()
        self.table = ttk.Frame(self.frame)
        self.table.grid()
        self.spots = []
        for row in range(3):
            for column in range(3):
                spot = ttk.Combobox(self.table, values=list(CARD_UI_TO_LOGIC.keys()), state='readonly')
                spot.grid(column=column, row=row)
                spot.bind('<<ComboboxSelected>>', self.validate)
                self.spots.append(spot)
        self.button = ttk.Button(self.frame, text="Auto", command=self.auto)
        self.button.grid(column=4, row=4)

    def validate(self, _):
        for spot in self.spots:
            if not spot.get():
                return
        self.start([CARD_UI_TO_LOGIC[spot.get()] for spot in self.spots])

    def auto(self):
        self.start()
        for index in range(9):
            self.spots[index].set(CARD_LOGIC_TO_UI[self.logic.table[index]])

    def start(self, table=None):
        self.logic = logic.Game(table)
        for spot in self.spots:
            spot.unbind('<<ComboboxSelected>>')
            spot.configure(state='disabled')
        self.button.configure(text="Recommend", command=self.recommend)

    def recommend(self):
        self.button.configure(state='disabled')
        best_spot, is_low = self.logic.get_best_move()
        self.recommendation = best_spot, is_low
        spot = self.spots[best_spot]
        spot.set('L' if is_low else 'H')
        spot.configure(state='readonly')
        spot.bind('<<ComboboxSelected>>', self.next_card)

    def next_card(self, event):
        spot = event.widget
        spot.unbind('<<ComboboxSelected>>')
        spot.configure(state='disabled')
        self.button.configure(state='normal')
        if self.logic.play_round(*self.recommendation, CARD_UI_TO_LOGIC[spot.get()]):
            self.spots[self.recommendation[0]].set(CARD_LOGIC_TO_UI[self.logic.table[self.recommendation[0]]])
        else:
            self.spots[self.recommendation[0]].set('X')

GAME = Game()
ROOT.mainloop()
