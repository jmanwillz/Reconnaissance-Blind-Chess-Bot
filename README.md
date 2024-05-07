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

Allows you to play against a bot. Useful for testing and debugging.

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

Allows you to watch a saved match.

```bash
rc-replay [-h] history_path
```

#### Round Robin

In order to play a round robin run the following command:

```bash
./round_robin.sh
```

This shell script looks as follows:

```bash
#!/bin/bash

# Define your Python command with arguments
rc_bot_match_command="rc-bot-match"

# Define different sets of arguments
argument_sets=(
    "baseline_agent.py reconchess.bots.trout_bot"
    "baseline_agent.py reconchess.bots.random_bot"
    "reconchess.bots.trout_bot baseline_agent.py"
    "reconchess.bots.random_bot baseline_agent.py"
    )

# Number of times to run each argument set
num_runs=5

# Loop through each set of arguments
for arguments in "${argument_sets[@]}"; do
    echo "Running with arguments: $arguments"

    # Extract individual arguments and replace spaces with underscores
    arguments_formatted=$(echo "$arguments" | sed 's/ /_/g')

    # Run the Python command multiple times with the same arguments
    for ((i=1; i<=$num_runs; i++)); do
        # Generate a timestamp
        timestamp=$(date +"%Y-%m-%d_%H-%M-%S")

        output_file="output_${timestamp}_${arguments_formatted}.txt"

        echo "Run $i"
        $rc_bot_match_command $arguments >> "$output_file"
    done
done

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
