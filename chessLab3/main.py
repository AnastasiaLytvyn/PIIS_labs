import chess
import random

class NegaAgent:
    board = None

    def __init__(self, board: chess.Board()):
        self.board = board

    def material_balance(self):
        white = self.board.occupied_co[chess.WHITE]
        black = self.board.occupied_co[chess.BLACK]
        return (
                chess.popcount(white & board.pawns) - chess.popcount(black & board.pawns) +
                3 * (chess.popcount(white & board.knights) - chess.popcount(black & board.knights)) +
                3 * (chess.popcount(white & board.bishops) - chess.popcount(black & board.bishops)) +
                5 * (chess.popcount(white & board.rooks) - chess.popcount(black & board.rooks)) +
                9 * (chess.popcount(white & board.queens) - chess.popcount(black & board.queens))
        )

    def numberOFPieces(self, whoToMove):
        if whoToMove == 1:
            chosen = self.board.occupied_co[chess.WHITE]
        else:
            chosen = self.board.occupied_co[chess.BLACK]
        return (
                chess.popcount(chosen & self.board.pawns) +
                (chess.popcount(chosen & self.board.knights)) +
                (chess.popcount(chosen & self.board.bishops)) +
                (chess.popcount(chosen & self.board.rooks)) +
                (chess.popcount(chosen & self.board.queens))
        )

    def evaluationFunction(self, whoToMove):
        numberOfWhites = self.numberOFPieces(1)
        numberOfBlacks = self.numberOFPieces(-1)
        materialBalance = self.material_balance()
        return materialBalance * (numberOfWhites - numberOfBlacks) * whoToMove

    def negaMax(self, depth: int, whoToMove: int, alpha, beta) -> tuple:
        if depth == 0:
            return self.evaluationFunction(whoToMove), None
        if alpha == float("-inf"):
          return self.minmaxScout(depth, whoToMove, alpha, beta)
        else:
          return self.minmax(depth, whoToMove)
        
    def minmax(self, depth: int, whoToMove: int):
      maxScore = -999
      bestMove = ''
      for legalMove in self.board.legal_moves:
            score = -(self.negaMax(depth - 1, -whoToMove)[0])
            if score == 0:
                score = random.random()
            if score > maxScore:
                maxScore = score
                bestMove = legalMove
      return maxScore, bestMove

    def minmaxScout(self, depth: int, whoToMove: int, alpha, beta):
      bestMove = None
      for legalMove in self.board.legal_moves:
          score = -(self.negaScout(depth - 1, -whoToMove, -beta, -alpha)[0])
          if score > alpha and score < beta and depth > 1:
              score2 = -(self.negaScout(depth - 1, -whoToMove, -beta, -score))[0]
              score = max(score, score2)
          if score == 0:
              score = random.random()
          if score > alpha:

              alpha = score
              bestMove = legalMove
          if alpha >= beta:
              return alpha, bestMove
          beta = alpha + 1
      return alpha, bestMove

board = chess.Board()
negaAgent = NegaAgent(board)
depth, whoToMove = 5, -1
choose = input("input 1 to play against negaMax and 2 for negaScout")

while not board.is_checkmate():
    print("Game state:\n")
    print(board)
    move = input("Input your move: ")
    board.push_san(move)
    if choose == 1:
      negaMove = negaAgent.negaMax(depth, whoToMove, 0, 0)[1]  
    elif choose == 2:
      negaMove = negaAgent.negaMax(depth, whoToMove, float("-inf"), float("inf"))[1]  
    board.push(negaMove)
