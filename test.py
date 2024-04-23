# Jason Wille (1352200), Kaylyn Karuppen (2465081), Reece Lazarus (2345362)

from main import get_board, make_move, get_possible_moves


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

    moves_1 = get_possible_moves(board_1)
    moves_2 = get_possible_moves(board_2)

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


def main():
    part_1_board_representation()
    print()
    part_1_move_execution()
    print()
    part_2_next_move_prediction()


if __name__ == "__main__":
    main()
