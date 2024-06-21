# Reconnaissance Blind Chess Bot

A custom implementation of a Reconnaissance Blind Chess bot using the library [reconchess](https://github.com/reconnaissanceblindchess/reconchess).

## Contributors

| ![Jason Wille](images/jason.jpeg "Jason Wille") <br/> [Jason Wille](https://www.linkedin.com/in/jasonwille97/) | ![Reece Lazarus](images/reece.jpeg "Reece Lazarus") <br/> [Reece Lazarus](https://www.linkedin.com/in/reecelaz/) | ![Kaylyn Karuppen](images/kaylyn.jpeg "Kaylyn Karuppen") <br/> [Kaylyn Karuppen](https://www.linkedin.com/in/kaylynkaruppen/) |
| :------------------------------------------------------------------------------------------------------------: | :--------------------------------------------------------------------------------------------------------------: | :---------------------------------------------------------------------------------------------------------------------------: |

## Installation

The python version being used was `3.9.7`.

In order to run the code you need to first install the required packages by running:

```bash
# Install dependencies.
pip install -r requirements.txt
```

The main file was used for part 1, part 2 and part 3 of the assignment. It can be run as follows:

```bash
# Run the main.py file.
python main.py
```

For each submission tests were written that passed if the functions worked for the given sample inputs. These tests can be run as follows:

```bash
# Run the unit tests for part 1, 2, & 3.
python test.py
```

## Playing Chess

Make sure to install Stockfish. On macOS this can be done as follows:

```bash
brew install stockfish
```

It is then important to set the environment variable `STOCKFISH_EXECUTABLE`. You can do this by placing the following in your `.bashrc` or `.zshrc`.

```bash
# Point your environment variable at the stockfish executable.
export STOCKFISH_EXECUTABLE=$(which stockfish)
```

#### RC Play

Allows you to play against a bot, using the built in script `rc-play`. Useful for testing and debugging.

```bash
# Play as white against the trout bot.
rc-play --color white reconchess.bots.trout_bot
```

In general the command looks as follows:

```bash
rc-play [-h] [--color {white,black,random}] [--seconds_per_player SECONDS_PER_PLAYER] bot_path
```

#### RC Bot Match

Playing two bots against each other is as easy as playing against your bot, using the built in script `rc-bot-match`.

```bash
# Put the baseline bot against the trout bot. The baseline bot will play as white.
rc-bot-match baseline_agent.py reconchess.bots.trout_bot
```

In general the command looks as follows:

```bash
rc-bot-match [-h] [--seconds_per_player SECONDS_PER_PLAYER] white_bot_path black_bot_path
```

#### RC Playback

The built in script `rc-playback` takes a game history, a bot, and the color the bot played as, and plays back the actions the bot took during the game. This allows you to exactly replicate the error producing conditions.

In general the command looks as follows:

```bash
rc-playback [-h] game_history_path bot_path {white,black}
```

#### RC Replay

Allows you to replay a saved match using the built in script `rc-replay`.

```bash
rc-replay [-h] history_path
```

#### Round Robin

In order to play a round robin use the following shell script:

```bash
./round_robin.sh
```

## Branching Strategy

- master
- development
  - feature/feature-name
  - bug/bug-name
