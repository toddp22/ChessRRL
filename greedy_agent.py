import chess
from random import shuffle

import evaluate_board

def get_move(board):
  best_move = None
  best_move_value = -10000
  color = board.turn
  moves = list(board.generate_legal_moves())
  shuffle(moves)

  for move in moves:
    board.push(move)
    if color == chess.WHITE:
      board_value = evaluate_board.evaluate(board)
    else:
      board_value = -evaluate_board.evaluate(board)
    board.pop()

    if board_value > best_move_value:
      best_move_value = board_value
      best_move = move

  return best_move
