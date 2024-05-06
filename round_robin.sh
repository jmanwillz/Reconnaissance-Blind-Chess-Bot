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
    # Generate a timestamp
    timestamp=$(date +"%Y-%m-%d_%H-%M-%S")
    output_file="output_$timestamp.txt"
    
    echo "Running with arguments: $arguments"
    
    # Run the Python command multiple times with the same arguments
    for ((i=1; i<=$num_runs; i++)); do
        echo "Run $i"
        $rc_bot_match_command $arguments >> "$output_file"
    done
done
