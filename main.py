# system packages
import chess

# custom modules
from lib.board_operations import generators
from lib.board_operations import serializers
from lib.agents import minimax_agent as black
from lib.agents import greedy_agent as white

board = generators.normal_board()

print(serializers.unicode(board))
while (not board.is_game_over()):
  if board.turn == chess.WHITE:
    move = white.get_move(board.copy())
  else:
    move = black.get_move(board.copy())
  board.push(move)
  print(serializers.unicode(board))

print(board.result())
