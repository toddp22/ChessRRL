# system packages
import chess

# custom modules
from lib.board_operations import generators
from lib.board_operations import serializers
from lib.agents import minimax_agent as white
from lib.agents import q_learning_agent as black

board = generators.random_krk_board()

print("New game!")
print(serializers.unicode(board))
while (not board.is_game_over()):
  if board.turn == chess.WHITE:
    move = white.get_move(board.copy(), depth=7)
  else:
    move = black.get_move(board.copy())
  board.push(move)
  print(serializers.unicode(board))

print(board.result())
