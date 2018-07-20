import chess
import numpy as np
import state_action_table_generator as satg
from board_operations import generators

Q = satg.state_action_table()
q_lookup = satg.state_map()
action_count = len(Q[0])

learning_rate = 0.8
y = 0.95
num_episodes = 2000

reward_list = []

def invalid_action(board_key, action_index):
  Q[board_key, action_index] = -999

def get_immediate_reward(b):
  r = 0
  if b.is_checkmate():
    r = 100
  if b.is_stalemate():
    r = -100
  if len(list(b.pieces(chess.ROOK, chess.WHITE))) == 0:
    r = -100
  return r

def get_valid_move(b, bk):
  action_index = np.argmax(Q[bk,:] + np.random.randn(1, action_count)*(1./(i+1)))
  action = satg.ACTIONS[action_index]
  action_piece = action[0]
  action_direction = action[1]
  action_square = list(b.pieces(action_piece.piece_type, action_piece.color))[0]
  result_square = action_square + action_direction

  if result_square >= 64 or result_square < 0:
    invalid_action(bk, action_index)
    return get_valid_move(b, bk)

  move = chess.Move(action_square, result_square)

  if move not in b.generate_legal_moves():
    invalid_action(bk, action_index)
    return get_valid_move(b, bk)

  return move, action_index

print("Begin!")
for i in range(num_episodes):
  b = generators.random_krk_board()
  reward_all = 0
  is_destination = False
  board_key = q_lookup[satg.board_key(b)]
  for j in range(1000):
    m,a = get_valid_move(b, board_key)
    b.push(m)
    immediate_reward = get_immediate_reward(b)
    is_destination = immediate_reward != 0

    new_board_key = q_lookup[satg.board_key(b)]

    Q[board_key,a] = Q[board_key,a] + learning_rate * (immediate_reward + y * np.max(Q[new_board_key,:]) - Q[board_key,a])

    reward_all += immediate_reward
    board_key = new_board_key
    if is_destination:
      print("reached destination!")
      break
  reward_list.append(reward_all)
  print("Score over time: " +  str(sum(reward_list)/num_episodes))
