import chess
import numpy as np

from .. import state_action_table_generator as satg

ACTIONS = satg.ACTIONS
STATE_MAP = satg.state_map()
Q = satg.from_file("state_action_table.bin")

def get_move(board):
  state = STATE_MAP[satg.board_key(board)]
  return legal_move(board, state)

def legal_move(board, state):
  action_index = np.nanargmax(Q[state,:])
  action = ACTIONS[action_index]
  action_piece = action[0]
  action_direction = action[1]
  square_set = list(board.pieces(action_piece.piece_type, action_piece.color))
  if len(square_set) == 0: return invalid_move(board, state, action_index)
  action_square = square_set[0]
  result_square = action_square + action_direction

  if result_square >= 64 or result_square < 0: return invalid_move(board, state, action_index)
  move = chess.Move(action_square, result_square)
  if move not in board.generate_legal_moves(): return invalid_move(board, state, action_index)

  print(action_index)
  print(Q[state,:])
  return move

def invalid_move(board, state, action_index):
  print("found invalid move (" + str(state) + "," + str(action_index) + ")")
  Q[state, action_index] = np.nan
  legal_move(board, state)
