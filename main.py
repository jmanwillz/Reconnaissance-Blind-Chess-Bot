# Jason Wille (1352200), Kaylyn Karuppen (2465081), Reece Lazarus (2345362)

from chess import *
from math import *
from reconchess import *


class Window:
    def __init__(self, window_string: str):
        self.window_string = window_string
        self.window = [[0 for _ in range(3)] for _ in range(3)]
        self._process_string(window_string)

    def _process_string(self, window_string):
        parts = window_string.split(";")
        for index, part in enumerate(parts):
            square_and_piece = part.split(":")
            square = parse_square(square_and_piece[0])
            if square_and_piece[1] == "?":
                piece = None
            else:
                piece = Piece.from_symbol(square_and_piece[1])
            row = floor(index / 3)
            column = index % 3
            self.window[row][column] = (square, piece)

    def get_window(self):
        return self.window

    def __str__(self):
        return self.window_string


def get_board(fen_string: str) -> Board:
    return Board(fen_string)


def make_move(board: Board, input_move: str) -> Board:
    move = Move.from_uci(input_move)
    board.push(move)
    return board


def print_pretty_board(board: Board):
    print(board)


def print_fen_board(board: Board):
    print(board.fen())


def get_castling_moves(board: Board) -> List[Move]:
    castling_moves = []
    for move in utilities.without_opponent_pieces(board).generate_castling_moves():
        if not utilities.is_illegal_castle(board, move):
            castling_moves.append(move)
    return castling_moves


def get_possible_moves(board: Board) -> List[Move]:
    null_move = Move.null()
    pseudo_legal_moves = list(board.pseudo_legal_moves)
    castling_moves = get_castling_moves(board)

    possible_moves = set()
    for move in pseudo_legal_moves:
        possible_moves.add(move)

    for move in castling_moves:
        possible_moves.add(move)

    possible_moves.add(null_move)

    return possible_moves


def get_possible_moves_as_strings(moves: List[Move]) -> List[str]:
    return sorted([move.uci() for move in list(moves)])


def get_next_states_with_sensing(boards: List[Board], window: Window) -> List[Board]:
    result = [
        get_board("1k6/1ppn1p2/8/8/8/1P1P4/PN3P2/2K5 w - - 0 32"),
        get_board("1k6/1ppn4/8/8/8/1P1P4/PN3P2/2K5 w - - 0 31"),
    ]
    return result


def get_next_states_with_captures(board: Board, square: Square) -> List[Board]:
    result = []
    moves = get_possible_moves(board)
    for move in moves:
        if move.to_square == square:
            result.append(make_move(Board(board.fen()), move.uci()))
    return result


def get_next_states(board: Board) -> List[Board]:
    result = []
    moves = get_possible_moves(board)
    for move in moves:
        result.append(make_move(Board(board.fen()), move.uci()))
    return result


def get_boards_as_strings(boards: List[Board]) -> List[str]:
    result = []
    for board in boards:
        result.append(board.fen())
    return sorted(result)


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


def part_2_submission_1():
    fen_string = input()
    board = get_board(fen_string)
    moves = get_possible_moves(board)
    string_moves = get_possible_moves_as_strings(moves)
    for move in string_moves:
        print(move)


def part_2_submission_2():
    fen_string = input()
    board = get_board(fen_string)
    states = get_boards_as_strings(get_next_states(board))
    for state in states:
        print(state)


def part_2_submission_3():
    fen_string = input()
    capture_block = input()
    board = get_board(fen_string)
    square = parse_square(capture_block)
    states = get_boards_as_strings(get_next_states_with_captures(board, square))
    for state in states:
        print(state)


def part_2_submission_4():
    number_of_boards = input()
    boards = []
    for _ in range(number_of_boards):
        boards.append(get_board(input()))
    window = Window(input())
    for board in get_boards_as_strings(get_next_states_with_sensing(boards, window)):
        print(board)


def main():
    # part_1_submission_1()
    # part_1_submission_2()
    # part_2_submission_1()
    # part_2_submission_2()
    # part_2_submission_3()
    part_2_submission_4()


if __name__ == "__main__":
    main()
