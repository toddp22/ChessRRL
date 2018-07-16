# pip install python-chess

# system packages
import chess

# custom modules
import board_generators
import board_display as display
import minimax_agent as black
import random_agent as white

board = board_generators.normal_board()

display.unicode(board)
while (not board.is_game_over()):
  if board.turn == chess.WHITE:
    move = white.get_move(board.copy())
  else:
    move = black.get_move(board.copy())
  board.push(move)
  display.unicode(board)

print(board.result())
