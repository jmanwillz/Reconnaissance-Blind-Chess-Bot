#!/bin/bash

# Check if the 'debug' argument is present
if [[ "$1" == "debug" ]]; then
    rc_bot_match_command="./run_remote_debugger.sh"
else
    rc_bot_match_command="rc-bot-match"
fi

# Define different sets of arguments
argument_sets=(
    "baseline_agent.py reconchess.bots.trout_bot"
    "reconchess.bots.trout_bot baseline_agent.py"
    "baseline_agent.py reconchess.bots.attacker_bot"
    "reconchess.bots.attacker_bot baseline_agent.py"
    "baseline_agent.py reconchess.bots.random_bot"
    "reconchess.bots.random_bot baseline_agent.py"
    )

# Number of times to run each argument set
num_runs=5

# Loop through each set of arguments
for arguments in "${argument_sets[@]}"; do
    # Extract individual arguments and replace spaces with underscores
    arguments_formatted=$(echo "$arguments" | sed 's/ /_/g')

    # Run the Python command multiple times with the same arguments
    for ((i=1; i<=$num_runs; i++)); do
        echo "Run $i for $arguments"
        
        if [[ "$1" == "debug" ]]; then
            echo "Waiting for debugger..."
        fi

        timestamp=$(date +"%Y-%m-%d_%H-%M-%S")
        output_file="output_${timestamp}_${arguments_formatted}.txt"
        $rc_bot_match_command $arguments | tee -a "$output_file"
    done
done
