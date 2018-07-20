import chess
import random
import pickle
import numpy as np

ACTIONS = (
  (chess.Piece.from_symbol('k'), 1),
  (chess.Piece.from_symbol('k'), -1),
  (chess.Piece.from_symbol('k'), 8),
  (chess.Piece.from_symbol('k'), -8),
  (chess.Piece.from_symbol('k'), 7),
  (chess.Piece.from_symbol('k'), -7),
  (chess.Piece.from_symbol('k'), 9),
  (chess.Piece.from_symbol('k'), -9),

  (chess.Piece.from_symbol('K'), 1),
  (chess.Piece.from_symbol('K'), -1),
  (chess.Piece.from_symbol('K'), 8),
  (chess.Piece.from_symbol('K'), -8),
  (chess.Piece.from_symbol('K'), 7),
  (chess.Piece.from_symbol('K'), -7),
  (chess.Piece.from_symbol('K'), 9),
  (chess.Piece.from_symbol('K'), -9),

  (chess.Piece.from_symbol('R'), 1),
  (chess.Piece.from_symbol('R'), 2),
  (chess.Piece.from_symbol('R'), 3),
  (chess.Piece.from_symbol('R'), 4),
  (chess.Piece.from_symbol('R'), 5),
  (chess.Piece.from_symbol('R'), 6),
  (chess.Piece.from_symbol('R'), 7),
  (chess.Piece.from_symbol('R'), -1),
  (chess.Piece.from_symbol('R'), -2),
  (chess.Piece.from_symbol('R'), -3),
  (chess.Piece.from_symbol('R'), -4),
  (chess.Piece.from_symbol('R'), -5),
  (chess.Piece.from_symbol('R'), -6),
  (chess.Piece.from_symbol('R'), -7),
  (chess.Piece.from_symbol('R'), 8),
  (chess.Piece.from_symbol('R'), 16),
  (chess.Piece.from_symbol('R'), 24),
  (chess.Piece.from_symbol('R'), 32),
  (chess.Piece.from_symbol('R'), 40),
  (chess.Piece.from_symbol('R'), 48),
  (chess.Piece.from_symbol('R'), 56),
  (chess.Piece.from_symbol('R'), -8),
  (chess.Piece.from_symbol('R'), -16),
  (chess.Piece.from_symbol('R'), -24),
  (chess.Piece.from_symbol('R'), -32),
  (chess.Piece.from_symbol('R'), -40),
  (chess.Piece.from_symbol('R'), -48),
  (chess.Piece.from_symbol('R'), -56)
)

def board_key(b):
  return (
    b.bishops,
    b.kings,
    b.knights,
    b.pawns,
    b.queens,
    b.rooks,
    b.occupied,
    b.occupied_co[chess.BLACK],
    b.occupied_co[chess.WHITE],
    int(b.turn)
  )

def state_action_table():
  return np.random.uniform(low=-0.05, high=0.05, size=(524_544, 44))

def is_duplicate_placement(i,j,k):
  if i == j: return True
  if i == k: return True
  if j == k: return True
  return False

def pieces():
  return [
    chess.Piece.from_symbol('K'),
    chess.Piece.from_symbol('R'),
    chess.Piece.from_symbol('k')
  ]

def record_state(states, board, count):
  board.turn = chess.WHITE
  states[board_key(board)] = count
  count += 1
  board.turn = chess.BLACK
  states[board_key(board)] = count
  count += 1
  return count

def state_map():
  states = {}
  count = 0
  board = chess.Board(None)
  
  for i in range(64):
    board.set_piece_at(i, pieces()[0])
    count = record_state(states, board, count)
    board.clear_board()

    board.set_piece_at(i, pieces()[1])
    count = record_state(states, board, count)
    board.clear_board()

    board.set_piece_at(i, pieces()[2])
    count = record_state(states, board, count)
    board.clear_board()

    for j in range(64):
      if is_duplicate_placement(i,j,None): continue

      board.set_piece_at(i, pieces()[0])
      board.set_piece_at(j, pieces()[1])
      count = record_state(states, board, count)
      board.clear_board()

      board.set_piece_at(i, pieces()[0])
      board.set_piece_at(j, pieces()[2])
      count = record_state(states, board, count)
      board.clear_board()

      board.set_piece_at(i, pieces()[1])
      board.set_piece_at(j, pieces()[2])
      count = record_state(states, board, count)
      board.clear_board()

      for k in range(64):
        if is_duplicate_placement(i,j,k): continue
  
        board.set_piece_at(i, pieces()[0])
        board.set_piece_at(j, pieces()[1])
        board.set_piece_at(k, pieces()[2])
  
        count = record_state(states, board, count)
        board.clear_board()
  return states

def serialize(name, data):
  f = open(name, 'wb')
  pickle.dump(data, f)
