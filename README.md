# Reconnaissance Blind Chess Bot

---

## Members

- Jason Wille
- Kaylyn Karuppen
- Reece Lazarus

---

## Branching Strategy

- master
- development
  - feature/feature-name
  - bug/bug-name

---

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

---

## Play against the trout bot

Make sure to install Stockfish. On macOS this can be done as follows:

```bash
brew install stockfish
```

It is then important to set the environment variable `STOCKFISH_EXECUTABLE`. You can do this by placing the following in your `.bashrc` or `.zshrc`.

```bash
export STOCKFISH_EXECUTABLE="/opt/homebrew/bin/stockfish"
```

You can then play against your bot by running:

```bash
rc-play trout_bot.py
```
