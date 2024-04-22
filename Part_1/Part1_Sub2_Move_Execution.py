#Part1 Sub1 Board Representation
#Jason Wille (1352200), Kaylyn Karuppen (2465081), Reece Lazarus (2345362)

import chess

fen = input()
input_move = input()

board = chess.Board(fen)

move = chess.Move.from_uci(input_move)
board.push(move)

print(board.fen())