# Reconnaissance Blind Chess Bot

## Members

- Jason Wille (1352200)
- Kaylyn Karuppen (2465081)
- Reece Lazarus (2345362)

## Branching Strategy

- master
- development
  - feature/feature-name
  - bug/bug-name

## Installation

The python version being used was 3.9.7.

In order to run the code you need to first install the required packages by running:

```bash
pip install -r requirements.txt
```

To run the code you can then execute the following command:

```bash
python main.py
```

## Playing Chess

Make sure to install Stockfish. On macOS this can be done as follows:

```bash
brew install stockfish
```

It is then important to set the environment variable `STOCKFISH_EXECUTABLE`. You can do this by placing the following in your `.bashrc` or `.zshrc`.

```bash
export STOCKFISH_EXECUTABLE=$(which stockfish)
```

You can then play against your bot by running:

```bash
rc-play trout_bot.py
```

To face off a bot against the trout bot run the following:

```bash
rc-bot-match reconchess.bots.random_bot trout_bot.py
```

To replay a game from the game history file use the following command:

```bash
rc-replay <path to saved game history file>
```

## Marks

- Part 1

  1. Board representation: 100% (5%)
  2. Move execution: 100% (5%)

- Part 2

  1. Next move prediction: 100% (5%)
  2. Next state prediction: 100% (5%)
  3. Next state prediction with captures: 100% (5%)
  4. Next state prediction with sensing: 100% (10%)

- Part 3

  1. Move generation: 100% (5%)
  2. Multiple move generation: 100% (5%)

- Part 4

  1. Baseline implementation: ?
  2. Report detailing improvements and round-robin tournament: ?
  3. Competitive portion: ?
