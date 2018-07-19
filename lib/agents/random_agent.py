import chess
import random

secure_random = random.SystemRandom()

def get_move(board):
  moves = list(board.generate_legal_moves())
  return secure_random.choice(moves)
