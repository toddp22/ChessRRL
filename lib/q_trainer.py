import chess
import numpy as np
import state_action_table_generator as satg
from board_operations import generators
from board_operations import serializers

Q = satg.state_action_table()
q_lookup = satg.state_map()
action_count = len(Q[0])

alpha = 0.8  # learning rate
gamma = 0.95 # discount factor
num_episodes = 5_000_000

reward_list = []

def print_status_update(board, immediate_reward, before_reward, state, action, old_state):
  last_board_unicode = serializers.unicode(board)
  board.pop()
  penultimate_board_unicode = serializers.unicode(board)
  print(penultimate_board_unicode)
  print(last_board_unicode)
  print("immediate_reward: " + str(immediate_reward))
  print("reward: " + str(before_reward) + " => " + str(Q[state,action]))
  print(Q[old_state,:])
  print("reached destination!")

def invalid_action(state, action_index):
  Q[state, action_index] = np.nan

def get_immediate_reward(board):
  r = 0
  if board.is_checkmate():
    r = 100
  if board.is_stalemate():
    r = -100
  if len(list(board.pieces(chess.ROOK, chess.WHITE))) == 0:
    r = -100
  return r

def get_valid_move(board, state):
  action_index = np.nanargmax(Q[state,:] + np.random.randn(action_count)*(np.float64(2 * num_episodes) / np.float64(i+1)))
  action = satg.ACTIONS[action_index]
  action_piece = action[0]
  action_direction = action[1]
  action_square = list(board.pieces(action_piece.piece_type, action_piece.color))[0]
  result_square = action_square + action_direction

  if result_square >= 64 or result_square < 0:
    invalid_action(state, action_index)
    return get_valid_move(board, state)

  move = chess.Move(action_square, result_square)

  if move not in board.generate_legal_moves():
    invalid_action(state, action_index)
    return get_valid_move(board, state)

  return move, action_index

np.set_printoptions(formatter={'float': '{: 0.3f}'.format})
print("Begin!")
for i in range(num_episodes):
  board = generators.random_krk_board()
  reward_all = 0
  is_destination = False
  state = q_lookup[satg.board_key(board)]
  print("----------\nnew game\n----------")
  for j in range(1000):
    move, action = get_valid_move(board, state)
    board.push(move)
    immediate_reward = get_immediate_reward(board)
    is_destination = immediate_reward != 0

    old_state = state
    new_state = q_lookup[satg.board_key(board)]

    before_reward = Q[state,action]
    Q[state,action] = Q[state,action] + alpha * (immediate_reward + gamma * np.nanmax(Q[new_state,:]) - Q[state,action])

    reward_all += immediate_reward
    state = new_state
    if is_destination:
      print_status_update(board, immediate_reward, before_reward, state, action, old_state)
      break
  reward_list.append(reward_all)
  print("Score over time: " +  str(sum(reward_list)/num_episodes))

satg.serialize("state_action_table.bin", Q)
