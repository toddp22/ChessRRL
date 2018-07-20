import chess
import numpy as np

def unicode(board):
  return board.unicode(invert_color=True) + "\n"

def krk_board_to_array(board):
  return np.concatenate((
    [((board.occupied_co[chess.BLACK] & board.kings)   >> bit) & 1 for bit in range(64)],
    [((board.occupied_co[chess.WHITE] & board.kings)   >> bit) & 1 for bit in range(64)],
    [((board.occupied_co[chess.WHITE] & board.rooks)   >> bit) & 1 for bit in range(64)],
    [board.turn]
  ), out=np.empty(193))

def board_to_array(board):
  return np.concatenate((
    [((board.occupied_co[chess.BLACK] & board.bishops) >> bit) & 1 for bit in range(64)],
    [((board.occupied_co[chess.BLACK] & board.kings)   >> bit) & 1 for bit in range(64)],
    [((board.occupied_co[chess.BLACK] & board.knights) >> bit) & 1 for bit in range(64)],
    [((board.occupied_co[chess.BLACK] & board.pawns)   >> bit) & 1 for bit in range(64)],
    [((board.occupied_co[chess.BLACK] & board.queens)  >> bit) & 1 for bit in range(64)],
    [((board.occupied_co[chess.BLACK] & board.rooks)   >> bit) & 1 for bit in range(64)],
    [((board.occupied_co[chess.WHITE] & board.bishops) >> bit) & 1 for bit in range(64)],
    [((board.occupied_co[chess.WHITE] & board.kings)   >> bit) & 1 for bit in range(64)],
    [((board.occupied_co[chess.WHITE] & board.knights) >> bit) & 1 for bit in range(64)],
    [((board.occupied_co[chess.WHITE] & board.pawns)   >> bit) & 1 for bit in range(64)],
    [((board.occupied_co[chess.WHITE] & board.queens)  >> bit) & 1 for bit in range(64)],
    [((board.occupied_co[chess.WHITE] & board.rooks)   >> bit) & 1 for bit in range(64)],
    [board.turn]
  ), out=np.empty(769))
