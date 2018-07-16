import chess
from random import shuffle

import evaluate_board

def get_move(board, depth=3):
  best_move = None
  best_move_value = -10000
  color = board.turn
  moves = list(board.generate_legal_moves())
  shuffle(moves)

  for move in moves:
    board.push(move)
    move_value = minimax(board, color, depth - 1, -10000, 10000)
    board.pop()

    if move_value > best_move_value:
      best_move_value = move_value
      best_move = move

  return best_move

def minimax(board, color, depth, alpha, beta, is_current_player=False):
  if depth == 0:
    if color == chess.WHITE:
      return evaluate_board.evaluate(board)
    else:
      return -evaluate_board.evaluate(board)

  moves = list(board.generate_legal_moves())
  shuffle(moves)

  if is_current_player:
    best_move = -10000
    for move in moves:
      board.push(move)
      best_move = max(best_move, minimax(board, color, depth - 1, alpha, beta, not is_current_player))
      board.pop()
      alpha = max(alpha, best_move)
      if beta <= alpha:
        return best_move
    return best_move
  else:
    best_move = 10000
    for move in moves:
      board.push(move)
      best_move = min(best_move, minimax(board, color, depth - 1, alpha, beta, not is_current_player))
      board.pop()
      beta = min(beta, best_move)
      if beta <= alpha:
        return best_move
    return best_move
