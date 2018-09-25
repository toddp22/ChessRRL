import chess
import numpy as np
import state_action_table_generator as satg
from board_operations import generators
from board_operations import serializers

np.set_printoptions(formatter={'float': '{: 0.3f}'.format})

Q = satg.state_action_table()
q_lookup = satg.state_map()
action_count = len(Q[0])

alpha = 0.8  # learning rate
gamma = 0.95 # discount factor
num_episodes = 10_000_000
is_4x4_game = True

def get_reward(board, state, action, new_state, immediate_reward):
  if immediate_reward != 0: return immediate_reward
  try:
    opponant_action_index = np.nanargmax(Q[new_state,:])
  except:
    print("EXCEPTION: opponant has no legal moves")
    print("white's move" if board.turn == chess.WHITE else "black's move")
    print(serializers.unicode(board))
    for _ in range(len(board.move_stack)):
      board.pop()
      print(serializers.unicode(board))
      raise

  opponant_move = generate_move_from_action(board, opponant_action_index)
  if opponant_move == None:
    invalid_action(new_state, opponant_action_index)
    return get_reward(board, state, action, new_state, immediate_reward)

  board.push(move)
  resulting_state = q_lookup[satg.board_key(board)]
  board.pop()

  learned = gamma * np.nanmax(Q[resulting_state,:]) # + immediate_reward

  return (1 - alpha) * Q[state,action] + alpha * learned

def print_status_update(board, immediate_reward, before_reward, reward, old_state, action):
  # last_board_unicode = serializers.unicode(board)
  # board.pop()
  # penultimate_board_unicode = serializers.unicode(board)
  # print(penultimate_board_unicode)
  # print(last_board_unicode)
  # print("winner: " + ("black" if board.turn == chess.BLACK else "white"))
  print("winner: " + ("white" if board.turn == chess.BLACK else "black"))
  # print("immediate_reward: " + str(immediate_reward))
  # print("reward: (" + str(reward) + ") " + str(before_reward) + " => " + str(Q[old_state,action]))
  # print(Q[old_state,:])
  # print("reached destination!")

def invalid_action(state, action_index):
  Q[state, action_index] = np.nan

def get_immediate_reward(board):
  turn_multiplier = 1 if board.turn == chess.BLACK else -1

  r = 0
  if board.is_checkmate():
    r = 100
  if board.is_stalemate():
    r = -100
  if len(board.pieces(chess.ROOK, chess.WHITE)) == 0:
    r = -100 # only two kings is an automatic stalemate
  if len(board.pieces(chess.KING, chess.BLACK)) == 0:
    r = 1 # we started with a bad board where black was already in check
  if r == 0 and get_valid_move(board) == None:
    # we're on a 4x4 board, so the python-chess board thinks we have
    # valid moves left, but in reality, if the board were actually
    # 4x4, then there wouldn't be any valid moves left
    if board.is_check():
      r = 100
    else:
      r = -100
  return r * turn_multiplier

def generate_move_from_action(board, action_index):
  action = satg.ACTIONS[action_index]
  action_piece = action[0]
  action_direction = action[1]
  square_set = list(board.pieces(action_piece.piece_type, action_piece.color))
  if len(square_set) == 0: return None # piece doesn't exist
  action_square = square_set[0]
  result_square = action_square + action_direction

  if result_square >= 64 or result_square < 0: return None # move not on board
  if is_4x4_game and not result_square in generators.VALID_4X4_POSITIONS: return None
  move = chess.Move(action_square, result_square)
  if move not in board.generate_legal_moves(): return None # move not legal

  return move

def get_valid_move(board):
  bstate = q_lookup[satg.board_key(board)]

  if len(Q[bstate,:][np.logical_not(np.isnan(Q[bstate,:]))]) == 0:
    return None

  try:
    action_index = np.nanargmax(Q[bstate,:] + np.random.randn(action_count)*(np.float64(2 * num_episodes) / np.float64(i+1)))
  except:
    print("EXCEPTION: num_moves: " + str(len(board.move_stack)))
    print("white's move" if board.turn == chess.WHITE else "black's move")
    print(serializers.unicode(board))
    for _ in range(len(board.move_stack)):
      board.pop()
      print(serializers.unicode(board))
      raise
  move = generate_move_from_action(board, action_index)

  if move == None:
    invalid_action(bstate, action_index)
    return get_valid_move(board)

  return move, action_index

print("Begin!")
for i in range(num_episodes):
  board = generators.random_krk_board(is_4x4_game)
  is_destination = get_immediate_reward(board) != 0
  if is_destination: continue
  state = q_lookup[satg.board_key(board)]
  for j in range(1000):
    try:
      move, action = get_valid_move(board)
    except:
      print(board.turn)
      print(board)
      import code; code.interact(local=dict(globals(), **locals()))
      raise
    board.push(move)
    immediate_reward = get_immediate_reward(board)
    is_destination = immediate_reward != 0

    old_state = state
    new_state = q_lookup[satg.board_key(board)]

    before_reward = Q[state,action]
    reward = get_reward(board,state,action,new_state,immediate_reward)
    Q[state,action] = reward

    state = new_state
    if is_destination:
      Q[state,:] = -reward # should be an impossible state since the game is over, but helps with training
      print_status_update(board, immediate_reward, before_reward, reward, old_state, action)
      break
  print("(" + str(i) + "/" + str(num_episodes) + ")")
  if ((1+i) % 100000 == 0):
    satg.serialize("state_action_table_" + str(i) + ".bin", Q)
