import chess
import random

def normal_board():
  return chess.Board()

def random_krk_board():
  secure_random = random.SystemRandom()
  board = chess.Board(None)
  piece_symbols = ['R', 'K', 'k']

  for piece_symbol in piece_symbols:
    piece = chess.Piece.from_symbol(piece_symbol)

    placement = secure_random.randrange(0,64)
    while board.piece_at(chess.SQUARES_180[placement]) != None:
      placement = secure_random.randrange(0,64)

    board.set_piece_at(chess.SQUARES_180[placement], piece)
  board.turn = secure_random.getrandbits(1)

  if board.is_checkmate():
    return random_krk_board()

  return board
