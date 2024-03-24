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

        ttk.Style().configure('higher.TCombobox', foreground='red')
        ttk.Style().configure('lower.TCombobox', foreground='blue')
        self.available_cards = list(CARD_UI_TO_LOGIC.keys())
        self.spots = []
        for row in range(3):
            for column in range(3):
                spot = ttk.Combobox(self.table, values=self.available_cards, state='readonly')
                spot.grid(column=column, row=row)
                spot.bind('<<ComboboxSelected>>', self.validate)
                self.spots.append(spot)
        self.spot_sizes = [1] * 9
        self.progress = -2
        self.progress_label = ttk.Label(self.table, text=f"Progress: {self.progress}")
        self.progress_label.grid(column=1, row=4)

        self.button = ttk.Button(self.frame, text="Auto", command=self.start)
        self.button.grid(column=4, row=4)

    def update_available_cards(self, available_cards):
        self.available_cards = available_cards
        for spot in self.spots:
            spot.configure(values=self.available_cards)

    def validate(self, _):
        found_cards = {card: 0 for card in CARD_UI_TO_LOGIC.keys()}
        available_cards = list(CARD_UI_TO_LOGIC.keys())
        valid = True
        for spot in self.spots:
            if not spot.get():
                valid = False
            else:
                found_cards[spot.get()] += 1
                if found_cards[spot.get()] == 4:
                    available_cards.remove(spot.get())
        self.update_available_cards(available_cards)
        if valid:
            self.start([CARD_UI_TO_LOGIC[spot.get()] for spot in self.spots])

    def start(self, table=None):
        self.button.grid_forget()
        self.logic = logic.Game(table)
        for index, spot in enumerate(self.spots):
            spot.unbind('<<ComboboxSelected>>')
            spot.configure(state='disabled')
            spot.set(CARD_LOGIC_TO_UI[self.logic.table[index]])
        self.recommend()

    def recommend(self):
        self.update_available_cards([CARD_LOGIC_TO_UI[card] for card in set(self.logic.deck)])
        best_spot, is_low = self.logic.recommend()
        self.recommendation = best_spot, is_low
        spot = self.spots[best_spot]
        spot.configure(state='readonly')
        if(is_low):
            spot.set(f"{spot.get()} (-)")
            spot.configure(style='lower.TCombobox')
        else:
            spot.set(f"{spot.get()} (+)")
            spot.configure(style='higher.TCombobox')
        spot.bind('<<ComboboxSelected>>', self.next_card)

    def next_card(self, event):
        self.spot_sizes[self.recommendation[0]] += 1
        spot = event.widget
        spot.unbind('<<ComboboxSelected>>')
        spot.configure(state='disabled', style='')
        if not self.logic.play_round(*self.recommendation, CARD_UI_TO_LOGIC[spot.get()]):
            self.progress += 6 - self.spot_sizes[self.recommendation[0]]
            self.progress_label.configure(text=f"Progress: {self.progress}")
            spot.set(f"{spot.get()} (X)")
            self.spots.pop(self.recommendation[0])
        self.recommend()

GAME = Game()
ROOT.mainloop()
