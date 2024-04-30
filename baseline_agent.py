# Jason Wille (1352200), Kaylyn Karuppen (2465081), Reece Lazarus (2345362)

from chess import *
from main import (
    get_next_states_with_capture,
    get_next_states_with_sensing,
    multiple_move_generation,
    get_strings_as_boards,
    is_on_edge,
    get_window_string,
)
from reconchess import *
from typing import Set

import os
import random

####################################################################################################################################################################################

STOCKFISH_ENV_VAR = "STOCKFISH_EXECUTABLE"

####################################################################################################################################################################################


def initialise_stockfish():
    stockfish_path = ""
    if STOCKFISH_ENV_VAR in os.environ:
        candidate_path = os.environ[STOCKFISH_ENV_VAR]
        if os.path.exists(candidate_path):
            stockfish_path = candidate_path
    if stockfish_path == "":
        stockfish_path = "/opt/stockfish/stockfish"
    return chess.engine.SimpleEngine.popen_uci(stockfish_path, setpgrp=True)


####################################################################################################################################################################################


class BaselineAgent(Player):
    def __init__(self):
        self.my_color: Color = None
        self.opponent_name: str = None
        self.my_piece_captured_square: Optional[Square] = None
        self.current_state: Board = None
        self.possible_states: Set[str] = set()
        self.engine = initialise_stockfish()

    def handle_game_start(self, color: Color, board: Board, opponent_name: str):
        self.my_color = color
        self.opponent_name = opponent_name
        self.current_state = board
        self.possible_states.add(self.current_state.fen())

    def handle_opponent_move_result(
        self, captured_my_piece: bool, capture_square: Optional[Square]
    ):
        self.my_piece_captured_square = capture_square
        if captured_my_piece:
            self.current_state.remove_piece_at(capture_square)
            for state in get_next_states_with_capture(
                self.current_state, capture_square
            ):
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
        for square, piece in sense_result:
            self.current_state.set_piece_at(square, piece)

        window_string = get_window_string(sense_result)

        for state in get_next_states_with_sensing(
            get_strings_as_boards(list(self.possible_states)), window_string
        ):
            self.possible_states.add(state.fen())

    def choose_move(
        self, move_actions: List[chess.Move], seconds_left: float
    ) -> Optional[chess.Move]:
        while len(self.possible_states) > 10000:
            self.possible_states.remove(random.choice(self.possible_states))

        stockfish_time = 10 / len(self.possible_states)

        return multiple_move_generation(
            get_strings_as_boards(list(self.possible_states)),
            self.engine,
            stockfish_time,
        )

    def handle_move_result(
        self,
        requested_move: Optional[chess.Move],
        taken_move: Optional[chess.Move],
        captured_opponent_piece: bool,
        capture_square: Optional[Square],
    ):
        if taken_move is not None:
            self.current_state.push(taken_move)

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
