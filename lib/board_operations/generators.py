import chess
import random

piece_symbols = ['R', 'K', 'k']
secure_random = random.SystemRandom()
positions_4x4 = [
   0,  1,  2,  3,
   8,  9, 10, 11,
  16, 17, 18, 19,
  24, 25, 26, 27
]

VALID_4X4_POSITIONS = [chess.SQUARES_180[position] for position in positions_4x4]

def normal_board():
  return chess.Board()

def random_krk_board(is_4x4_game=False):
  board = chess.Board(None)

  for piece_symbol in piece_symbols:
    piece = chess.Piece.from_symbol(piece_symbol)

    while True:
      if is_4x4_game:
        placement = secure_random.choice(positions_4x4)
      else:
        placement = secure_random.randrange(0,64)
      if board.piece_at(chess.SQUARES_180[placement]) == None: break

    board.set_piece_at(chess.SQUARES_180[placement], piece)
  board.turn = secure_random.getrandbits(1)

  if board.is_checkmate() or board.is_stalemate() or (not board.is_valid()):
    return random_krk_board(is_4x4_game)

  return board
