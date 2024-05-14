# Jason Wille (1352200), Kaylyn Karuppen (2465081), Reece Lazarus (2345362)

from main import (
    get_boards_as_strings,
    get_next_states,
    get_next_states_with_capture,
    get_next_states_with_sensing,
    get_strings_as_boards,
    get_window_string,
    is_on_edge,
    multiple_move_generation,
    visualize_boards,
)

from test import bcolors

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
