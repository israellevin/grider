# grider

Helper for playing a solitaire card game.

## Requirements

You will need Python3 with Tkinter to run this program.

For debian-based systems, you can install it with:
```sh
apt install python3-tk
```

For Mac OS, you can install it with:
```sh
brew install python-tk
```

## Running

This will run iterations of random games using our strategy and print the success rate:

```sh
./logic.py [number of iterations, defaulting to 1,000]
```

This will run a GUI for you to play the game and get strategic recommendations:

```sh
./ui.py
```
