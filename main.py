# Jason Wille (1352200), Kaylyn Karuppen (2465081), Reece Lazarus (2345362)

from chess import *
from datetime import datetime
from fentoboardimage import *
from math import *
from reconchess import *

import chess.engine
import os

########################################################################################################################

STOCKFISH_ENV_VAR = "STOCKFISH_EXECUTABLE"

########################################################################################################################


def visualize_boards(boards: List[Board]):
    os.makedirs("states", exist_ok=True)
    for index, board in enumerate(boards):
        boardImage = fenToImage(
            fen=board.fen(),
            squarelength=100,
            pieceSet=loadPiecesFolder("./pieces"),
            darkColor="#D18B47",
            lightColor="#FFCE9E",
        )
        boardImage.save(
            os.path.join(
                "states", f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_{index}.png"
            )
        )


def get_square_not_on_edge(square_on_edge: Square) -> Square:
    rank = square_rank(square_on_edge)
    file = square_file(square_on_edge)

    if rank == 0:
        rank += 1
    elif rank == 7:
        rank -= 1

    if file == 0:
        file += 1
    elif file == 7:
        file -= 1

    return square(file, rank)


def get_best_sense_from_piece_distribution(
    piece_distribution, number_of_states: int
) -> Optional[Square]:
    for square in piece_distribution.keys():
        array_length = len(piece_distribution[square])
        set_of_pieces = set(piece_distribution[square])
        set_length = len(set_of_pieces)
        piece_distribution[square] = {
            "array": piece_distribution[square],
            "array_length": array_length,
            "set": set_of_pieces,
            "set_length": set_length,
        }

    ordered_squares = [
        k
        for k, _ in sorted(
            piece_distribution.items(),
            key=lambda item: item[1]["set_length"],
            reverse=True,
        )
    ]

    for square in ordered_squares:
        if (piece_distribution[square]["array_length"] == number_of_states) and (
            piece_distribution[square]["set_length"] == 1
        ):
            continue

        if piece_distribution[square]["set_length"] > 1:
            if is_on_edge(square):
                return get_square_not_on_edge(square)
            return square

    return None


def merge_piece_distribution_with_new_map(
    piece_distribution: dict, new_map: dict, color: Color
) -> dict:
    result = dict()
    for key in piece_distribution.keys():
        result[key] = piece_distribution[key]
    for key in new_map.keys():
        if key in result.keys():
            if new_map[key].color == color:
                result[key].append(new_map[key])
        else:
            if new_map[key].color == color:
                result[key] = [new_map[key]]
    return result


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


def get_next_states_with_capture(board: Board, square: Square) -> List[Board]:
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


def get_strings_as_boards(board_strings: List[str]) -> List[Board]:
    result = []
    for board_string in board_strings:
        result.append(get_board(board_string))
    return result


def is_on_edge(square: Square) -> bool:
    file, rank = square_file(square), square_rank(square)
    return file in {0, 7} or rank in {0, 7}


def get_window_string(sense_result: List[Tuple[Square, Optional[chess.Piece]]]) -> str:
    window_str = ""
    for part in sense_result:
        window_str += square_name(part[0]) + ":"
        if part[1] is None:
            window_str += "?"
        else:
            window_str += part[1].symbol()
        window_str += ";"
    return window_str[:-1]


def initialise_stockfish(local):
    stockfish_path = "/opt/stockfish/stockfish"

    if not local:
        return chess.engine.SimpleEngine.popen_uci(stockfish_path, setpgrp=True)

    if STOCKFISH_ENV_VAR in os.environ:
        stockfish_path = os.environ[STOCKFISH_ENV_VAR]
    else:
        raise KeyError(f"The environment variable {STOCKFISH_ENV_VAR} does not exist.")

    if not os.path.exists(stockfish_path):
        raise ValueError(f"The path {stockfish_path} does not exist.")

    return chess.engine.SimpleEngine.popen_uci(stockfish_path, setpgrp=True)


def generate_move(board: Board, stockfish_engine, stockfish_time=0.1) -> Optional[Move]:
    friendly_king_square = board.king(board.turn)
    enemy_king_square = board.king(not board.turn)

    if enemy_king_square == None or friendly_king_square == None:
        return None

    if enemy_king_square:
        enemy_king_attackers = board.attackers(board.turn, enemy_king_square)
        if enemy_king_attackers:
            attacker_square = enemy_king_attackers.pop()
            return chess.Move(attacker_square, enemy_king_square)

    try:
        board.clear_stack()
        result = stockfish_engine.play(board, chess.engine.Limit(time=stockfish_time))
        return result.move
    except chess.engine.EngineTerminatedError:
        print("Agent: Stockfish Engine Died")
    except chess.engine.EngineError:
        print(f"Agent: Stockfish Engine bad state at {board.fen()}")

    return None


def multiple_move_generation(
    boards: List[Board], stockfish_engine, stockfish_time=0.1
) -> Optional[Move]:
    move_dict = dict()
    for board in boards:
        new_move = generate_move(board, stockfish_engine, stockfish_time)
        if new_move != None:
            new_move = new_move.uci()
            if new_move in move_dict:
                move_dict[new_move] = move_dict[new_move] + 1
            else:
                move_dict[new_move] = 1

    if len(move_dict.keys()) == 0:
        return None

    sorted_move_dict = dict(sorted(move_dict.items()))
    max_move = max(sorted_move_dict, key=sorted_move_dict.get)
    return Move.from_uci(max_move)


########################################################################################################################


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
    states = get_boards_as_strings(get_next_states_with_capture(board, square))
    for state in states:
        print(state)


def part_2_submission_4():
    number_of_boards = int(input())
    boards = []
    for _ in range(number_of_boards):
        boards.append(get_board(input()))
    for board in get_boards_as_strings(get_next_states_with_sensing(boards, input())):
        print(board)


def part_3_submission_1(local):
    fen_string = input()
    board = get_board(fen_string)
    stockfish_engine = initialise_stockfish(local)
    move = generate_move(board, stockfish_engine)
    print(move)
    stockfish_engine.quit()


def part_3_submission_2(local):
    number_of_boards = int(input())
    boards = []
    for _ in range(number_of_boards):
        boards.append(get_board(input()))
    stockfish_engine = initialise_stockfish(local)
    move = multiple_move_generation(boards, stockfish_engine)
    print(move)
    stockfish_engine.quit()


########################################################################################################################


def main():
    # part_1_submission_1()
    # part_1_submission_2()
    # part_2_submission_1()
    # part_2_submission_2()
    # part_2_submission_3()
    # part_2_submission_4()
    # part_3_submission_1(local=False)
    part_3_submission_2(local=False)


if __name__ == "__main__":
    main()
