import chess

values = {
  'P': 10, 'p': -10,
  'N': 30, 'n': -30,
  'B': 30, 'b': -30,
  'R': 50, 'r': -50,
  'Q': 90, 'q': -90,
  'K': 900,'k': -900
}

def evaluate(board):
  score = 0

  for i in range(64):
    piece = board.piece_at(i)
    if piece == None: continue
    score += values[piece.symbol()]

  return score
