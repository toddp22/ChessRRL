import chess
import random

ACTIONS = (
  (chess.Piece.from_symbol('K'), 1),
  (chess.Piece.from_symbol('K'), -1),
  (chess.Piece.from_symbol('K'), 8),
  (chess.Piece.from_symbol('K'), -8),
  (chess.Piece.from_symbol('K'), 7),
  (chess.Piece.from_symbol('K'), -7),
  (chess.Piece.from_symbol('K'), 9),
  (chess.Piece.from_symbol('K'), -9),

  (chess.Piece.from_symbol('R'), 1),
  (chess.Piece.from_symbol('R'), 2),
  (chess.Piece.from_symbol('R'), 3),
  (chess.Piece.from_symbol('R'), 4),
  (chess.Piece.from_symbol('R'), 5),
  (chess.Piece.from_symbol('R'), 6),
  (chess.Piece.from_symbol('R'), 7),
  (chess.Piece.from_symbol('R'), -1),
  (chess.Piece.from_symbol('R'), -2),
  (chess.Piece.from_symbol('R'), -3),
  (chess.Piece.from_symbol('R'), -4),
  (chess.Piece.from_symbol('R'), -5),
  (chess.Piece.from_symbol('R'), -6),
  (chess.Piece.from_symbol('R'), -7),
  (chess.Piece.from_symbol('R'), 8),
  (chess.Piece.from_symbol('R'), 16),
  (chess.Piece.from_symbol('R'), 24),
  (chess.Piece.from_symbol('R'), 32),
  (chess.Piece.from_symbol('R'), 40),
  (chess.Piece.from_symbol('R'), 48),
  (chess.Piece.from_symbol('R'), 56),
  (chess.Piece.from_symbol('R'), -8),
  (chess.Piece.from_symbol('R'), -16),
  (chess.Piece.from_symbol('R'), -24),
  (chess.Piece.from_symbol('R'), -32),
  (chess.Piece.from_symbol('R'), -40),
  (chess.Piece.from_symbol('R'), -48),
  (chess.Piece.from_symbol('R'), -56)
)

secure_random = random.SystemRandom()

def generate_action_array(number_of_states):
  return [secure_random.uniform(-0.05, 0.05) for _ in range(number_of_states)]

def is_duplicate_placement(i,j,k):
  if i == j: return True
  if i == k: return True
  if j == k: return True
  return False

pieces = [
  chess.Piece.from_symbol('K'),
  chess.Piece.from_symbol('R'),
  chess.Piece.from_symbol('k')
]

states = {}

for i in range(64):
  for j in range(64):
    for k in range(64):
      if is_duplicate_placement(i,j,k): continue

      board = chess.Board(None)

      board.set_piece_at(i, pieces[0])
      board.set_piece_at(j, pieces[1])
      board.set_piece_at(k, pieces[2])

      fen_string = board.fen().split(" ")[0]

      states[fen_string] = generate_action_array(len(ACTIONS))

for state in states:
  print(str(state)+ " " + str(states[state]))
