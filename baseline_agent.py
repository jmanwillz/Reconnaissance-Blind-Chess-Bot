# Jason Wille (1352200), Kaylyn Karuppen (2465081), Reece Lazarus (2345362)

from chess import *
from reconchess import *
from typing import Set

import os
import random

########################################################################################################################

STOCKFISH_ENV_VAR = "STOCKFISH_EXECUTABLE"

########################################################################################################################


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


def initialise_stockfish():
    stockfish_path = ""
    if STOCKFISH_ENV_VAR in os.environ:
        candidate_path = os.environ[STOCKFISH_ENV_VAR]
        if os.path.exists(candidate_path):
            stockfish_path = candidate_path
    if stockfish_path == "":
        stockfish_path = "/opt/stockfish/stockfish"
    return chess.engine.SimpleEngine.popen_uci(stockfish_path, setpgrp=True)


def make_move(board: Board, input_move: str) -> Board:
    move = Move.from_uci(input_move)
    board.push(move)
    return board


def get_castling_moves(board: Board) -> List[Move]:
    castling_moves = []
    for move in utilities.without_opponent_pieces(board).generate_castling_moves():
        if not utilities.is_illegal_castle(board, move):
            castling_moves.append(move)
    return castling_moves


def get_strings_as_boards(board_strings: List[str]) -> List[Board]:
    result = []
    for board_string in board_strings:
        result.append(get_board(board_string))
    return result


def get_board(fen_string: str) -> Board:
    return Board(fen_string)


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


def generate_move(board: Board, stockfish_engine, stockfish_time=0.1) -> Optional[Move]:
    enemy_king_square = board.king(not board.turn)
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
        print("Stockfish Engine died")
    except chess.engine.EngineError:
        print('Stockfish Engine bad state at "{}"'.format(board.fen()))

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


class BaselineAgent(Player):
    def __init__(self):
        # random.seed(10)
        self.first_turn = True
        self.my_color: Color = None
        self.opponent_name: str = None
        self.possible_states: Set[str] = set()
        self.engine = initialise_stockfish()

    def handle_game_start(self, color: Color, board: Board, opponent_name: str):
        self.my_color = color
        self.opponent_name = opponent_name
        self.possible_states.add(board.fen())

    def handle_opponent_move_result(
        self, captured_my_piece: bool, capture_square: Optional[Square]
    ):
        if self.my_color == WHITE and self.first_turn:
            self.first_turn = False
            # This is the start turn.
            return
        else:
            if not captured_my_piece:
                # If the opponent didn't capture my piece they could have made any move.
                possible_states_as_boards = get_strings_as_boards(
                    list(self.possible_states)
                )
                self.possible_states = set()
                for board in possible_states_as_boards:
                    # It is the opponents turn.
                    board.turn = not self.my_color
                    next_states = get_next_states(board)
                    for state in next_states:
                        self.possible_states.add(state.fen())
                return
            else:
                possible_states_as_boards = get_strings_as_boards(
                    list(self.possible_states)
                )
                self.possible_states = set()
                for board in possible_states_as_boards:
                    board.turn = not self.my_color
                    states_after_capture = get_next_states_with_capture(
                        board, capture_square
                    )
                    for state in states_after_capture:
                        self.possible_states.add(state.fen())

    def choose_sense(
        self,
        sense_actions: List[Square],
        move_actions: List[chess.Move],
        seconds_left: float,
    ) -> Optional[Square]:
        while True:
            if len(sense_actions) == 0:
                return None
            sense_choice: Square = random.choice(sense_actions)
            sense_actions.remove(sense_choice)
            if not is_on_edge(sense_choice):
                return sense_choice

    def handle_sense_result(
        self, sense_result: List[Tuple[Square, Optional[chess.Piece]]]
    ):
        window_string = get_window_string(sense_result)
        possible_states_as_boards = get_strings_as_boards(list(self.possible_states))
        next_states_with_sensing = get_next_states_with_sensing(
            possible_states_as_boards, window_string
        )

        self.possible_states = set()
        for state in next_states_with_sensing:
            self.possible_states.add(state.fen())

    def choose_move(
        self, move_actions: List[chess.Move], seconds_left: float
    ) -> Optional[chess.Move]:
        while len(self.possible_states) > 10000:
            self.possible_states.remove(random.choice(list(self.possible_states)))

        stockfish_time = 10 / len(self.possible_states)
        possible_states_as_boards = get_strings_as_boards(list(self.possible_states))

        for board in possible_states_as_boards:
            board.turn = self.my_color

        chosen_move = multiple_move_generation(
            possible_states_as_boards,
            self.engine,
            stockfish_time,
        )

        if chosen_move in move_actions:
            return chosen_move
        else:
            print(f"Tried to make move: {chosen_move}")

        return None

    def handle_move_result(
        self,
        requested_move: Optional[chess.Move],
        taken_move: Optional[chess.Move],
        captured_opponent_piece: bool,
        capture_square: Optional[Square],
    ):
        if taken_move is not None:
            possible_states_as_boards = get_strings_as_boards(
                list(self.possible_states)
            )
            self.possible_states = set()
            for board in possible_states_as_boards:
                board.turn = self.my_color
                board.push(taken_move)
                self.possible_states.add(board.fen())

    def handle_game_end(
        self,
        winner_color: Optional[Color],
        win_reason: Optional[WinReason],
        game_history: GameHistory,
    ):
        try:
            self.engine.quit()
        except chess.engine.EngineTerminatedError:
            pass
