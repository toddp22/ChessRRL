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
winning_boards = []

board_logging_enabled = False
alpha = 0.8  # learning rate
gamma = 0.95 # discount factor
is_4x4_game = True
num_episodes = 10_000_000
probability_constant = 1.0
use_book_exploration_policy = True
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
    print("EXCEPTION: opponant has no legal moves. num_moves: " + str(len(board.move_stack)))
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

  board.push(opponant_move)
  resulting_state = q_lookup[satg.board_key(board)]
  board.pop()

  learned = gamma * np.nanmax(Q[resulting_state,:])

  return (1 - alpha) * Q[state,action] + alpha * learned

def invalid_action(state, action_index):
  Q[state, action_index] = np.nan

def get_immediate_reward(board, state, i):
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
  if r == 0 and get_valid_move(board, state, i) == None:
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
  try:
    if use_book_exploration_policy:
      k_raised_by_a = lambda a: 0 if np.isnan(a) else probability_constant ** a
      array = Q[state,:]
      minimum = np.min(array)
      if minimum < 0:
        array = array - minimum

      numerators = list(map(k_raised_by_a, array))

      if len(Q[state,:][np.logical_not(np.isnan(Q[state,:]))]) == 0: return None
      action_index = probability_choice(numerators)
    else:
      if len(Q[state,:][np.logical_not(np.isnan(Q[state,:]))]) == 0: return None
      action_index = np.nanargmax(Q[state,:] + np.random.randn(action_count)*(np.float64(2 * num_episodes) / np.float64(i+1)))
  except:
    print("EXCEPTION: num_moves: " + str(len(board.move_stack)))
    print("iteration: " + str(i))
    print("white's move" if board.turn == chess.WHITE else "black's move")
    print(serializers.unicode(board))
    for _ in range(len(board.move_stack)):
      board.pop()
      print(serializers.unicode(board))
    raise
  move = generate_move_from_action(board, action_index)

  if move == None:
    invalid_action(state, action_index)
    return get_valid_move(board, state, i)

  return move, action_index

def upgrade_probability_constant():
  global probability_constant
  probability_constant += 0.01
  print("upgrading probability_constant to " + str(probability_constant))

def start():
  total_black_wins = 0
  false_black_wins_last_100 = 0
  results = np.zeros(100, dtype=np.int)
  black_wins = []
  print("Begin!")
  for i in range(num_episodes):
    board = generators.random_krk_board(is_4x4_game)
    state = q_lookup[satg.board_key(board)]
    is_destination = get_immediate_reward(board, state, i) != 0
    winner = 0
    while(not is_destination):
      move, action = get_valid_move(board, state, i)
      board.push(move)

      old_state = state
      state = q_lookup[satg.board_key(board)]

      immediate_reward = get_immediate_reward(board, state, i)
      is_destination = immediate_reward != 0

      if is_destination:
        winning_boards.append(board.copy())
        if board.turn == chess.BLACK:
          if immediate_reward > 0: winner = chess.WHITE
          else: winner = chess.BLACK
        else:
          if immediate_reward > 0: winner = chess.BLACK
          else: winner = chess.WHITE
  
      reward = get_reward(board,old_state,action,state,immediate_reward)
      Q[old_state,action] = reward
  
      if is_destination: Q[state,:] = -reward # should be an impossible state since the game is over, but helps with training

    if is_destination and len(board.move_stack) > 0:
      if winner == chess.WHITE:
        results[i % 100] = 1
      else:
        results[i % 100] = 2
        black_wins.append(board.copy())
        total_black_wins += 1
        if len(board.move_stack) == 1 and board.turn == chess.WHITE:
          total_black_wins -= 1
          false_black_wins_last_100 += 1
    else:
      results[i % 100] = 0

    if i % 100 == 0:
      unique, counts = np.unique(results, return_counts=True)
      result = dict(zip(unique, counts))
      white_wins_last_100 = result.get(1, 0)
      black_wins_last_100 = result.get(2, 0)
      total_wins_last_100 = white_wins_last_100 + black_wins_last_100
      if total_wins_last_100 == 0:
        print("No wins in the past 100 games.")
      else:
        if board_logging_enabled:
          for b in winning_boards: print(serializers.unicode(b))
          print("~~~~~~~~~~~~BLACK WINS~~~~~~~~~~~~~")
          for b in black_wins:
            print("----------------------------------")
            print("num moves: " + str(len(b.move_stack)))
            print("turn: " + str(b.turn))
            print(serializers.unicode(b))
            for _ in range(len(b.move_stack)):
              b.pop()
              print(serializers.unicode(b))
            print("(end)")
        white_wins_percent = 100 * white_wins_last_100/total_wins_last_100
        black_wins_percent = 100 * black_wins_last_100/total_wins_last_100
        fixed_total = total_wins_last_100 - false_black_wins_last_100
        fixed_white_percent = 100 * white_wins_last_100/fixed_total
        fixed_black_percent = 100 * (black_wins_last_100 - false_black_wins_last_100)/fixed_total
        print("White wins: " + str(white_wins_percent) + "% || Black wins: " + str(black_wins_percent) + "% || Total wins: " + str(total_wins_last_100))
        print("White wins: " + str(white_wins_last_100) + " || Black wins: " + str(black_wins_last_100) + " || False black wins: " + str(false_black_wins_last_100))
        print("fixed: White: " + str(fixed_white_percent) + "% || fixed black: " + str(fixed_black_percent) + "% || fixed total: " + str(fixed_total))
        print("TOTAL BLACK WINS: " + str(total_black_wins) + " (" + str(total_black_wins / num_episodes) + "%)")
        print("(" + str(i) + "/" + str(num_episodes) + ")")
        if fixed_white_percent > 100.0: raise Exception("White fixed percent too high")
      winning_boards.clear()
      black_wins.clear()
      false_black_wins_last_100 = 0
    if (1+i) % 10000 == 0: upgrade_probability_constant()
    if ((1+i) % 100000 == 0): satg.serialize("state_action_table_" + str(i) + ".bin", Q)

start()
