# Jason Wille (1352200), Kaylyn Karuppen (2465081), Reece Lazarus (2345362)

from chess import *
from math import *
from reconchess import *

####################################################################################################################################################################################


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


def get_next_states_with_sensing(boards: List[Board], window: str) -> List[Board]:
    result = []
    for board in boards:
        is_valid = True
        for block in window.split(";"):
            block = block.split(":")
            square = parse_square(block[0])
            if block[1] != "?":
                piece = Piece.from_symbol(block[1])
            else:
                piece = None
            actual_piece = board.piece_at(square)
            if actual_piece != piece:
                is_valid = False
                break
        if is_valid:
            result.append(board)
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


####################################################################################################################################################################################


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
    for board in get_boards_as_strings(get_next_states_with_sensing(boards, input())):
        print(board)


####################################################################################################################################################################################


def main():
    # part_1_submission_1()
    # part_1_submission_2()
    # part_2_submission_1()
    # part_2_submission_2()
    # part_2_submission_3()
    part_2_submission_4()


if __name__ == "__main__":
    main()
