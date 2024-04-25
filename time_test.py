# Jason Wille (1352200), Kaylyn Karuppen (2465081), Reece Lazarus (2345362)

from datetime import datetime
from numpy import average, std

import json
import os
import subprocess
import time

OUTPUT_FOLDER = "time_trial"


def single_run(input: str):
    command = f'python main.py <<< "{input}"'
    start_time = time.time()
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    end_time = time.time()
    time_taken = end_time - start_time
    print(
        f"Move {result.stdout.strip()} took {round(time_taken, 4)} seconds with the input {input}."
    )
    return time_taken


def multiple_runs(number_of_runs, input):
    results = []
    start_time = time.time()
    for _ in range(number_of_runs):
        time_taken = single_run(input)
        results.append(time_taken)
    end_time = time.time()
    batch_time = end_time - start_time

    result_dictionary = dict()
    result_dictionary["total_time"] = batch_time
    result_dictionary["sum_of_run_times"] = sum(results)
    result_dictionary["average_run_time"] = average(results)
    result_dictionary["deviation_of_run_times"] = std(results)
    result_dictionary["run_times"] = results
    return result_dictionary


def run_experiment(number_of_runs, inputs):
    result = dict()
    for input in inputs:
        result[input] = multiple_runs(number_of_runs, input)
    return result


def save_data(result):
    date_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"{OUTPUT_FOLDER}_{date_time}.json"
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
    with open(os.path.join(OUTPUT_FOLDER, file_name), "w") as json_file:
        json.dump(result, json_file, indent=4)


def main():
    inputs = [
        "8/8/8/8/k7/8/7K/3B4 w - - 48 32",
        "k7/p2p1p2/P2P1P2/8/8/8/8/7K b - - 23 30",
        "rn3rk1/pbppq1pp/1p2pb2/4N2Q/3PN3/3B4/PPP2PPP/R3K2R w KQ - 7 11",
    ]
    number_of_runs = 15
    save_data(run_experiment(number_of_runs, inputs))


if __name__ == "__main__":
    main()
