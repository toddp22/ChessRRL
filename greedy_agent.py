import chess

import minimax_agent

def get_move(board):
  return minimax_agent.get_move(board, depth=1)
