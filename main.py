# Jason Wille (1352200), Kaylyn Karuppen (2465081), Reece Lazarus (2345362)

from chess import *
from reconchess import *


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


def get_castling_moves(board: Board) -> List[Move]:
    castling_moves = []
    for move in utilities.without_opponent_pieces(board).generate_castling_moves():
        if not utilities.is_illegal_castle(board, move):
            castling_moves.append(move)
    return castling_moves


def get_possible_moves(board: Board) -> List[str]:
    null_move = Move.null()
    pseudo_legal_moves = list(board.pseudo_legal_moves)
    castling_moves = get_castling_moves(board)

    possible_moves = set()
    for move in pseudo_legal_moves:
        possible_moves.add(move)

    for move in castling_moves:
        possible_moves.add(move)

    possible_moves.add(null_move)

    return sorted([move.uci() for move in list(possible_moves)])


def test():
    test_string_1 = "8/5k2/8/8/8/p1p1p2n/P1P1P3/RB2K2R w K - 12 45"
    test_string_2 = "8/8/8/8/7q/p2p1p1k/P2P1P2/Rn2K2R w KQ - 23 30"
    board = get_board(test_string_1)
    moves = get_possible_moves(board)
    for move in moves:
        print(move)


def main():
    # part_1_submission_1()
    # part_1_submission_2()
    test()


if __name__ == "__main__":
    main()
