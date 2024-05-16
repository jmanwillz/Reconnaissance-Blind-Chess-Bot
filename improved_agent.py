# Jason Wille (1352200), Kaylyn Karuppen (2465081), Reece Lazarus (2345362)

from chess import *
from datetime import datetime
from reconchess import *
from typing import Set

import chess.engine
import os
import random
import time

########################################################################################################################

STOCKFISH_ENV_VAR = "STOCKFISH_EXECUTABLE"

########################################################################################################################


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


def get_board(fen_string: str) -> Board:
    return Board(fen_string)


def get_strings_as_boards(board_strings: List[str]) -> List[Board]:
    result = []
    for board_string in board_strings:
        result.append(get_board(board_string))
    return result


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


def get_boards_as_strings(boards: List[Board]) -> List[str]:
    result = []
    for board in boards:
        result.append(board.fen())
    return sorted(result)


def get_next_states(board: Board) -> List[Board]:
    result = []
    moves = get_possible_moves(board)
    for move in moves:
        result.append(make_move(Board(board.fen()), move.uci()))
    return result


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


def initialise_stockfish():
    stockfish_path = ""
    if STOCKFISH_ENV_VAR in os.environ:
        candidate_path = os.environ[STOCKFISH_ENV_VAR]
        if os.path.exists(candidate_path):
            stockfish_path = candidate_path
    if stockfish_path == "":
        stockfish_path = "/opt/stockfish/stockfish"
    return chess.engine.SimpleEngine.popen_uci(stockfish_path, setpgrp=True)


########################################################################################################################


class ImprovedAgent(Player):
    def handle_game_start(self, color: Color, board: Board, opponent_name: str):
        self.engine = initialise_stockfish()
        self.first_turn = True
        self.my_color: Color = color
        self.my_piece_captured_square: Optional[Square] = None
        self.opponent_name: str = opponent_name
        self.possible_states: Set[Board] = {board.fen()}
        self.random_seed = time.time()
        self.start_time = datetime.now()
        random.seed(self.random_seed)

    def log_start(self):
        color = "Black"
        if self.my_color:
            color = "White"

        with open("seeds.txt", "a") as file:
            file.write(
                f"The seed used against {self.opponent_name} at {datetime.now()} where my color was {self.my_color} is: {self.random_seed}\n"
            )

        print(f"We are playing as: \t{color}")
        print(f"Random seed: \t\t{self.random_seed}")
        print(f"Opponent name: \t\t{self.opponent_name}")
        print()

    def log_state_change(self, boards_before: List[Board]):
        delta = len(self.possible_states) - len(boards_before)
        current_time = datetime.now()

        print(f"Before: \t\t{len(boards_before)}")

        if delta > 0:
            print(f"Change: \t\t{bcolors.FAIL}+{delta}{bcolors.ENDC}")
        elif delta < 0:
            print(f"Change: \t\t{bcolors.OKGREEN}{delta}{bcolors.ENDC}")
        else:
            print(f"Change: \t\t{bcolors.OKBLUE}{delta}{bcolors.ENDC}")

        print(f"After:  \t\t{len(self.possible_states)}")
        print()
        print(
            f"Time:   \t\t{bcolors.UNDERLINE}{current_time.strftime('%H:%M:%S')}{bcolors.ENDC}"
        )
        print(
            f"Elapsed time: \t\t{bcolors.UNDERLINE}{current_time - self.start_time}{bcolors.ENDC}"
        )
        print()

    def handle_opponent_move_result(
        self, captured_my_piece: bool, capture_square: Optional[Square]
    ):
        self.my_piece_captured_square = capture_square
        if self.first_turn and self.my_color == WHITE:
            self.log_start()
            self.first_turn = False
            return

        possible_boards: List[Board] = get_strings_as_boards(list(self.possible_states))
        self.possible_states = set()

        for board in possible_boards:
            board.turn = not self.my_color
            new_boards: List[Board] = []

            if captured_my_piece:
                # The opponent captured a piece of ours.
                new_boards = get_next_states_with_capture(board, capture_square)
            else:
                # The opponent did not capture a piece of ours.
                new_boards = get_next_states(board)

            self.possible_states.update(get_boards_as_strings(new_boards))

        if captured_my_piece:
            capture_square_name = square_name(capture_square)
        else:
            capture_square_name = "None"

        print(
            f"Move (Opponent): \t{self.opponent_name} (Capture: {capture_square_name})"
        )
        self.log_state_change(possible_boards)

    def choose_sense(
        self,
        sense_actions: List[Square],
        move_actions: List[Move],
        seconds_left: float,
    ) -> Optional[Square]:
        # if our piece was just captured, sense where it was captured
        if self.my_piece_captured_square:
            return self.my_piece_captured_square

        possible_boards: List[Board] = get_strings_as_boards(list(self.possible_states))
        piece_distribution = dict()
        for board in possible_boards:
            piece_distribution = merge_piece_distribution_with_new_map(
                piece_distribution, board.piece_map(), not self.my_color
            )

        sense_choice_from_dist: Optional[Square] = (
            get_best_sense_from_piece_distribution(
                piece_distribution, len(possible_boards)
            )
        )
        if sense_choice_from_dist is not None:
            return sense_choice_from_dist

        # sense at the move that we would have made with our current knowledge
        future_move = self.choose_move(move_actions, seconds_left)
        if future_move is not None:
            return future_move.to_square

        # otherwise, just randomly choose a sense action that isn't on the edge of the board
        while True:
            if len(sense_actions) == 0:
                return None
            sense_choice: Square = random.choice(sense_actions)
            sense_actions.remove(sense_choice)
            if not is_on_edge(sense_choice):
                return sense_choice

    def handle_sense_result(self, sense_result: List[Tuple[Square, Optional[Piece]]]):
        window_string: str = get_window_string(sense_result)
        possible_boards: List[Board] = get_strings_as_boards(list(self.possible_states))
        self.possible_states = set(
            get_boards_as_strings(
                get_next_states_with_sensing(possible_boards, window_string)
            )
        )

        print(f"Sensing (Me): \t\t{window_string}")
        self.log_state_change(possible_boards)

    def choose_move(
        self, move_actions: List[Move], seconds_left: float
    ) -> Optional[Move]:
        if len(self.possible_states) == 0:
            return None
        while len(self.possible_states) > 10000:
            self.possible_states.remove(random.choice(list(self.possible_states)))

        stockfish_time = 10 / len(self.possible_states)
        possible_boards: List[Board] = get_strings_as_boards(list(self.possible_states))

        for board in possible_boards:
            board.turn = self.my_color

        chosen_move = multiple_move_generation(
            possible_boards,
            self.engine,
            stockfish_time,
        )

        if chosen_move in move_actions:
            return chosen_move

        return None

    def handle_move_result(
        self,
        requested_move: Optional[Move],
        taken_move: Optional[Move],
        captured_opponent_piece: bool,
        capture_square: Optional[Square],
    ):
        possible_boards: List[Board] = get_strings_as_boards(list(self.possible_states))
        self.possible_states = set()

        for candidate_board in possible_boards:
            candidate_board.turn = self.my_color

            # If the taken move can't be made, the board is illegal.
            if taken_move not in candidate_board.pseudo_legal_moves:
                if taken_move != None:
                    continue

            # If the requested move and taken move are different, the requested move should be illegal.
            if requested_move != taken_move:
                if requested_move in candidate_board.pseudo_legal_moves:
                    continue

            # If I captured an opponent piece, there should be a piece on that block of the opponents color.
            if captured_opponent_piece:
                if candidate_board.color_at(capture_square) != (not self.my_color):
                    continue

            # If candidate board has piece there, then it should record as capture.
            opponent_color = not self.my_color
            if taken_move != None:
                if candidate_board.color_at(taken_move.to_square) == opponent_color:
                    if not captured_opponent_piece:
                        continue

            if taken_move != None:
                candidate_board.push(taken_move)
            candidate_board.turn = not self.my_color
            self.possible_states.add(candidate_board.fen())

        print(f"Move (Me): \t\t{type(self).__name__} (Move: {taken_move})")
        self.log_state_change(possible_boards)

    def handle_game_end(
        self,
        winner_color: Optional[Color],
        win_reason: Optional[WinReason],
        game_history: GameHistory,
    ):
        if (winner_color != None) and (win_reason != None):
            if winner_color == self.my_color:
                print(f"We won and the reason was {win_reason.name}")
            else:
                print(f"The opponent won and the reason was {win_reason.name}")

        try:
            self.engine.quit()
        except chess.engine.EngineTerminatedError:
            print(f"The engine terminated with an error.")
