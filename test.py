# Jason Wille (1352200), Kaylyn Karuppen (2465081), Reece Lazarus (2345362)

from chess import *
from reconchess import *

from main import (
    get_board,
    make_move,
    get_possible_moves,
    get_possible_moves_as_strings,
    get_next_states,
    get_boards_as_strings,
    get_next_states_with_captures,
    get_next_states_with_sensing,
)

####################################################################################################################################################################################


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


####################################################################################################################################################################################


def part_1_board_representation():
    print("Testing Part 1 - Board Representation")

    count = 0
    input_1 = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    input_2 = "r1bqkb1r/pppp1Qpp/2n2n2/4p3/2B1P3/8/PPPP1PPP/RNB1K1NR b KQkq - 0 4"

    board_1 = str(get_board(input_1))
    board_2 = str(get_board(input_2))

    board_1_result = "r n b q k b n r\np p p p p p p p\n. . . . . . . .\n. . . . . . . .\n. . . . . . . .\n. . . . . . . .\nP P P P P P P P\nR N B Q K B N R"
    board_2_result = "r . b q k b . r\np p p p . Q p p\n. . n . . n . .\n. . . . p . . .\n. . B . P . . .\n. . . . . . . .\nP P P P . P P P\nR N B . K . N R"

    if board_1 == board_1_result:
        print(f"\t- {bcolors.OKGREEN}Passed{bcolors.ENDC} Sample Input 1")
        count += 1
    else:
        print(f"\t- {bcolors.FAIL}Failed{bcolors.ENDC} Sample Input 1")

    if board_2 == board_2_result:
        print(f"\t- {bcolors.OKGREEN}Passed{bcolors.ENDC} Sample Input 2")
        count += 1
    else:
        print(f"\t- {bcolors.FAIL}Failed{bcolors.ENDC} Sample Input 2")

    print(f"\t- Passed {round(count / 2 * 100, 2)}% of tests for Board Representation")


def part_1_move_execution():
    print("Testing Part 1 - Move Execution")

    count = 0
    input_1 = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    move_1 = "e2e4"
    input_2 = "8/8/8/2k5/4K3/8/8/8 w - - 4 45"
    move_2 = "e4e5"

    board_1 = get_board(input_1)
    board_2 = get_board(input_2)
    board_1_after_move = make_move(board_1, move_1).fen()
    board_2_after_move = make_move(board_2, move_2).fen()

    board_1_fen_solution = "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1"
    board_2_fen_solution = "8/8/8/2k1K3/8/8/8/8 b - - 5 45"

    if board_1_after_move == board_1_fen_solution:
        print(f"\t- {bcolors.OKGREEN}Passed{bcolors.ENDC} Sample Input 1")
        count += 1
    else:
        print(f"\t- {bcolors.FAIL}Failed{bcolors.ENDC} Sample Input 1")

    if board_2_after_move == board_2_fen_solution:
        print(f"\t- {bcolors.OKGREEN}Passed{bcolors.ENDC} Sample Input 2")
        count += 1
    else:
        print(f"\t- {bcolors.FAIL}Failed{bcolors.ENDC} Sample Input 2")

    print(f"\t- Passed {round(count / 2 * 100, 2)}% of tests for Move Execution")


def part_2_next_move_prediction():
    print("Testing Part 2 - Next Move Prediction")

    count = 0
    input_1 = "8/5k2/8/8/8/p1p1p2n/P1P1P3/RB2K2R w K - 12 45"
    input_2 = "8/8/8/8/7q/p2p1p1k/P2P1P2/Rn2K2R w KQ - 23 30"

    board_1 = get_board(input_1)
    board_2 = get_board(input_2)

    moves_1 = get_possible_moves_as_strings(get_possible_moves(board_1))
    moves_2 = get_possible_moves_as_strings(get_possible_moves(board_2))

    moves_1_solution = [
        "0000",
        "e1d1",
        "e1d2",
        "e1f1",
        "e1f2",
        "e1g1",
        "h1f1",
        "h1g1",
        "h1h2",
        "h1h3",
    ]
    moves_2_solution = [
        "0000",
        "a1b1",
        "e1d1",
        "e1e2",
        "e1f1",
        "e1g1",
        "h1f1",
        "h1g1",
        "h1h2",
        "h1h3",
    ]

    if moves_1 == moves_1_solution:
        print(f"\t- {bcolors.OKGREEN}Passed{bcolors.ENDC} Sample Input 1")
        count += 1
    else:
        print(f"\t- {bcolors.FAIL}Failed{bcolors.ENDC} Sample Input 1")

    if moves_2 == moves_2_solution:
        print(f"\t- {bcolors.OKGREEN}Passed{bcolors.ENDC} Sample Input 2")
        count += 1
    else:
        print(f"\t- {bcolors.FAIL}Failed{bcolors.ENDC} Sample Input 2")

    print(f"\t- Passed {round(count / 2 * 100, 2)}% of tests for Next Move Prediction")


def part_2_next_state_prediction():
    print("Testing Part 2 - Next State Prediction")

    count = 0
    input_1 = "8/8/8/8/k7/8/7K/3B4 w - - 48 32"
    input_2 = "k7/p2p1p2/P2P1P2/8/8/8/8/7K b - - 23 30"
    output_1_result = "8/8/8/7B/k7/8/7K/8 b - - 49 32\n8/8/8/8/B7/8/7K/8 b - - 0 32\n8/8/8/8/k5B1/8/7K/8 b - - 49 32\n8/8/8/8/k7/1B6/7K/8 b - - 49 32\n8/8/8/8/k7/5B2/7K/8 b - - 49 32\n8/8/8/8/k7/6K1/8/3B4 b - - 49 32\n8/8/8/8/k7/7K/8/3B4 b - - 49 32\n8/8/8/8/k7/8/2B4K/8 b - - 49 32\n8/8/8/8/k7/8/4B2K/8 b - - 49 32\n8/8/8/8/k7/8/6K1/3B4 b - - 49 32\n8/8/8/8/k7/8/7K/3B4 b - - 49 32\n8/8/8/8/k7/8/8/3B2K1 b - - 49 32\n8/8/8/8/k7/8/8/3B3K b - - 49 32"
    output_2_result = "1k6/p2p1p2/P2P1P2/8/8/8/8/7K w - - 24 31\n8/pk1p1p2/P2P1P2/8/8/8/8/7K w - - 24 31\nk7/p2p1p2/P2P1P2/8/8/8/8/7K w - - 24 31"

    board_1 = get_board(input_1)
    board_2 = get_board(input_2)

    states_1 = get_boards_as_strings(get_next_states(board_1))
    states_2 = get_boards_as_strings(get_next_states(board_2))

    states_1_result = output_1_result.split("\n")
    states_2_result = output_2_result.split("\n")

    if states_1 == states_1_result:
        print(f"\t- {bcolors.OKGREEN}Passed{bcolors.ENDC} Sample Input 1")
        count += 1
    else:
        print(f"\t- {bcolors.FAIL}Failed{bcolors.ENDC} Sample Input 1")

    if states_2 == states_2_result:
        print(f"\t- {bcolors.OKGREEN}Passed{bcolors.ENDC} Sample Input 2")
        count += 1
    else:
        print(f"\t- {bcolors.FAIL}Failed{bcolors.ENDC} Sample Input 2")

    print(f"\t- Passed {round(count / 2 * 100, 2)}% of tests for Next State Prediction")


def part_2_next_state_prediction_with_captures():
    print("Testing Part 2 - Next State Prediction with Captures")

    count = 0
    fen_string_1 = "k1n1n3/p2p1p2/P2P1P2/8/8/8/8/7K b - - 23 30"
    fen_string_2 = (
        "r1bqk2r/pppp1ppp/2n2n2/4p3/1b2P3/1P3N2/PBPP1PPP/RN1QKB1R w KQkq - 0 5"
    )
    capture_block_1 = "d6"
    capture_block_2 = "e5"

    solution_1 = "k1n5/p2p1p2/P2n1P2/8/8/8/8/7K w - - 0 31\nk3n3/p2p1p2/P2n1P2/8/8/8/8/7K w - - 0 31"
    solution_2 = "r1bqk2r/pppp1ppp/2n2n2/4B3/1b2P3/1P3N2/P1PP1PPP/RN1QKB1R b KQkq - 0 5\nr1bqk2r/pppp1ppp/2n2n2/4N3/1b2P3/1P6/PBPP1PPP/RN1QKB1R b KQkq - 0 5"

    board_1 = get_board(fen_string_1)
    board_2 = get_board(fen_string_2)

    states_1 = get_boards_as_strings(
        get_next_states_with_captures(board_1, parse_square(capture_block_1))
    )
    states_2 = get_boards_as_strings(
        get_next_states_with_captures(board_2, parse_square(capture_block_2))
    )

    states_1_result = solution_1.split("\n")
    states_2_result = solution_2.split("\n")

    if states_1 == states_1_result:
        print(f"\t- {bcolors.OKGREEN}Passed{bcolors.ENDC} Sample Input 1")
        count += 1
    else:
        print(f"\t- {bcolors.FAIL}Failed{bcolors.ENDC} Sample Input 1")

    if states_2 == states_2_result:
        print(f"\t- {bcolors.OKGREEN}Passed{bcolors.ENDC} Sample Input 2")
        count += 1
    else:
        print(f"\t- {bcolors.FAIL}Failed{bcolors.ENDC} Sample Input 2")

    print(
        f"\t- Passed {round(count / 2 * 100, 2)}% of tests for Next State Prediction with Captures"
    )


def part_2_next_state_prediction_with_sensing():
    print("Testing Part 2 - Next State Prediction with Sensing")

    count = 0
    fen_strings = [
        "1k6/1ppn4/8/8/8/1P1P4/PN3P2/2K5 w - - 0 32",
        "1k6/1ppnP3/8/8/8/1P1P4/PN3P2/2K5 w - - 0 32",
        "1k6/1ppn1p2/8/8/8/1P1P4/PN3P2/2K5 w - - 0 32",
    ]
    window_string = "c8:?;d8:?;e8:?;c7:p;d7:n;e7:?;c6:?;d6:?;e6:?"
    solution = "1k6/1ppn1p2/8/8/8/1P1P4/PN3P2/2K5 w - - 0 32\n1k6/1ppn4/8/8/8/1P1P4/PN3P2/2K5 w - - 0 32"

    boards = []
    for fen_string in fen_strings:
        boards.append(get_board(fen_string))

    states = get_boards_as_strings(get_next_states_with_sensing(boards, window_string))

    if states == solution.split("\n"):
        print(f"\t- {bcolors.OKGREEN}Passed{bcolors.ENDC} Sample Input 1")
        count += 1
    else:
        print(f"\t- {bcolors.FAIL}Failed{bcolors.ENDC} Sample Input 1")

    print(
        f"\t- Passed {round(count / 1 * 100, 2)}% of tests for Next State Prediction with Sensing"
    )


####################################################################################################################################################################################


def main():
    part_1_board_representation()
    print()
    part_1_move_execution()
    print()
    part_2_next_move_prediction()
    print()
    part_2_next_state_prediction()
    print()
    part_2_next_state_prediction_with_captures()
    print()
    part_2_next_state_prediction_with_sensing()


if __name__ == "__main__":
    main()
