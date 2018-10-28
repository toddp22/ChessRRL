import random
import chess
import numpy as np
import state_action_table_generator as satg
from board_operations import generators
from board_operations import serializers

np.set_printoptions(formatter={'float': '{: 0.3f}'.format})
secure_random = random.SystemRandom()

Q = satg.state_action_table()
q_lookup = satg.state_map()
action_count = len(Q[0])
results = np.zeros(100, dtype=np.int)
winning_boards = []

alpha = 0.8  # learning rate
gamma = 0.95 # discount factor
num_episodes = 50_000_000
probability_constant = 1.1
#
# Probability Equation (page 379 Machine Learning book)
#
# P(a_i|s) = (k^(Q(s,a_i)))/(sum_j(k^(Q(s,a_j))))
# where
# k = probability_constant
# Q = Q

def get_reward(board, state, action, new_state, immediate_reward):
  if immediate_reward != 0: return immediate_reward
  try:
    opponant_action_index = np.nanargmax(Q[new_state,:])
  except:
    print("EXCEPTION: num_moves: " + str(len(board.move_stack)))
    print("white's move" if board.turn == chess.WHITE else "black's move")
    print(serializers.unicode(board))
    for _ in len(board.move_stack):
      board.pop()
      print(serializers.unicode(board))
    raise
  opponant_move = generate_move_from_action(board, opponant_action_index)
  if opponant_move == None:
    invalid_action(new_state, opponant_action_index)
    return get_reward(board, state, action, new_state, immediate_reward)

  board.push(opponant_move)
  resulting_state = q_lookup[satg.board_key(board)]
  board.pop()

  learned = gamma * np.nanmax(Q[resulting_state,:]) # + immediate_reward

  return (1 - alpha) * Q[state,action] + alpha * learned

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
  move = chess.Move(action_square, result_square)
  if move not in board.generate_legal_moves(): return None # move not legal

  return move

def probability_choice(probabilities):
  total_prob = sum(probabilities)
  chosen = secure_random.uniform(0, total_prob)
  cumulative = 0
  for index, probability in enumerate(probabilities):
    cumulative += probability
    if cumulative > chosen:
      return index
  raise Exception("probability_choice failed")

def get_valid_move(board, state, i):
  k_raised_by_a = lambda a: 0 if np.isnan(a) else probability_constant ** a
  array = Q[state,:]
  minimum = np.min(array)
  if minimum < 0:
    array = array - minimum

  numerators = list(map(k_raised_by_a, array))

  try:
    # bstate = q_lookup[satg.board_key(board)]
    # if len(Q[bstate,:][np.logical_not(np.isnan(Q[bstate,:]))]) == 0: return None
    # action_index = np.nanargmax(Q[bstate,:] + np.random.randn(action_count)*(np.float64(2 * num_episodes) / np.float64(i+1)))
    action_index = probability_choice(numerators)
  except:
    print("EXCEPTION: num_moves: " + str(len(board.move_stack)))
    print("white's move" if board.turn == chess.WHITE else "black's move")
    print(serializers.unicode(board))
    for _ in len(board.move_stack):
      board.pop()
      print(serializers.unicode(board))
      raise
  move = generate_move_from_action(board, action_index)

  if move == None:
    invalid_action(state, action_index)
    return get_valid_move(board, state, i)

  return move, action_index

def start():
  print("Begin!")
  for i in range(num_episodes):
    board = generators.random_krk_board()
    is_destination = False
    state = q_lookup[satg.board_key(board)]
    winner = 0
    for j in range(1000):
      move, action = get_valid_move(board, state, i)
      board.push(move)
      immediate_reward = get_immediate_reward(board)
      if immediate_reward != 0:
        winning_boards.append(board.copy())
        if board.turn == chess.BLACK:
          if immediate_reward > 0: winner = chess.WHITE
          else: winner = chess.BLACK
        else:
          if immediate_reward > 0: winner = chess.BLACK
          else: winner = chess.WHITE
      is_destination = immediate_reward != 0
  
      old_state = state
      state = q_lookup[satg.board_key(board)]
  
      reward = get_reward(board,old_state,action,state,immediate_reward)
      Q[old_state,action] = reward
  
      if is_destination:
        Q[state,:] = -reward # should be an impossible state since the game is over, but helps with training
        break
    if is_destination:
      if winner == chess.WHITE:
        results[i % 100] = 1
      else:
        results[i % 100] = 2
    else:
      results[i % 100] = 0
    if i % 100 == 0:
      unique, counts = np.unique(results, return_counts=True)
      result = dict(zip(unique, counts))
      total_wins = result.get(1, 0) + result.get(2, 0)
      if total_wins == 0:
        print("No wins in the past 100 games.")
      else:
        print(
          "White wins: " + str(100 * result.get(1, 0)/total_wins) + "% || Black wins: " + str(100 * result.get(2, 0)/total_wins) + "% || Total wins: " + str(total_wins)
        )
        print("(" + str(i) + "/" + str(num_episodes) + ")")
        for b in winning_boards:
          print(serializers.unicode(b))
        winning_boards.clear()
    if ((1+i) % 100000 == 0):
      satg.serialize("a_state_action_table_" + str(i) + ".bin", Q)

start()
