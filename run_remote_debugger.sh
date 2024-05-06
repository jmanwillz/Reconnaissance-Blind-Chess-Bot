#!/bin/bash

# Define the allowed values for arguments
allowed_values=("baseline_agent.py" "reconchess.bots.trout_bot" "reconchess.bots.random_bot")

# Function to check if a value is in the allowed list
is_allowed_value() {
    local value=$1
    for allowed_value in "${allowed_values[@]}"; do
        if [ "$value" = "$allowed_value" ]; then
            return 0  # Value is allowed
        fi
    done
    return 1  # Value is not allowed
}

# Check if the correct number of arguments is provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 white_bot black_bot"
    exit 1
fi

# Check if the arguments are among the allowed values
if ! is_allowed_value "$1"; then
    echo "Error: White bot is not one of the allowed values"
    exit 1
fi

if ! is_allowed_value "$2"; then
    echo "Error: Black bot is not one of the allowed values"
    exit 1
fi

# Assign arguments to variables
arg1=$1
arg2=$2

# Run the Python script with the provided arguments
python -m debugpy --listen localhost:8765 --wait-for-client -m reconchess.scripts.rc_bot_match "$arg1" "$arg2" --seconds_per_player 900000