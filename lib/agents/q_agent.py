import chess
import numpy
import state_action_table_generator as satg

Q = satg.state_action_table()
q_lookup = satg.state_map()
is_4x4_game = True

def get_move(board):
  bstate = q_lookup[satg.board_key(board)]
  action_index = np.nanargmax(Q[bstate,:])
