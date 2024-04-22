import chess


def get_board(fen_string):
    return chess.Board(fen_string)


def make_move(board, input_move):
    move = chess.Move.from_uci(input_move)
    board.push(move)
    return board


def print_pretty_board(board):
    print(board)


def print_fen_board(board):
    print(board.fen())


def part_1_submission_1():
    fen_string = input()
    board = get_board(fen_string)
    print_pretty_board(board)


def part_1_submission_2():
    fen_string = input()
    board = get_board(fen_string)
    input_move = input()
    board_after_move = make_move(board, input_move)
    print_fen_board(board_after_move)


def main():
    part_1_submission_1()
    # part_1_submission_2()


if __name__ == "__main__":
    main()
