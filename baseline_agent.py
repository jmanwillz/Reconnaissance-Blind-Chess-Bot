# Jason Wille (1352200), Kaylyn Karuppen (2465081), Reece Lazarus (2345362)

from chess import *
from datetime import datetime

from main import (
    get_next_states_with_capture,
    get_next_states_with_sensing,
    multiple_move_generation,
    get_strings_as_boards,
    is_on_edge,
    get_window_string,
    get_next_states,
    visualize_boards,
)

from reconchess import *
from typing import Set

import chess.engine
import datetime
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


class BaselineAgent(Player):
    def __init__(self):
        self.random_seed = time.time()
        random.seed(self.random_seed)
        print(f"The random seed being used is: {self.random_seed}")
        print()

        self.first_turn = True
        self.my_color: Color = None
        self.opponent_name: str = None
        self.possible_states: Set[str] = set()
        self.engine = initialise_stockfish()

    def handle_game_start(self, color: Color, board: Board, opponent_name: str):
        self.my_color = color
        self.opponent_name = opponent_name
        self.possible_states.add(board.fen())
        with open("seeds.txt", "a") as file:
            file.write(
                f"The seed used against {opponent_name} at {datetime.now()} where my color was {self.my_color} is: {self.random_seed}\n"
            )

    def handle_opponent_move_result(
        self, captured_my_piece: bool, capture_square: Optional[Square]
    ):
        if self.my_color == WHITE and self.first_turn:
            # This is the start turn.
            self.first_turn = False
            return
        else:
            print(f"{self.opponent_name} made a move.")
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
                # If the opponent did capture my piece they could only have made moves that could capture there.
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
                return

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

        return

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

        return None

    def handle_move_result(
        self,
        requested_move: Optional[chess.Move],
        taken_move: Optional[chess.Move],
        captured_opponent_piece: bool,
        capture_square: Optional[Square],
    ):
        print(f"Baseline Agent made the move: {taken_move}")
        if taken_move is not None:
            possible_states_as_boards = get_strings_as_boards(
                list(self.possible_states)
            )
            self.possible_states = set()
            for board in possible_states_as_boards:
                board.turn = self.my_color
                if taken_move in board.pseudo_legal_moves:
                    board.push(taken_move)
                    self.possible_states.add(board.fen())
            return

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
