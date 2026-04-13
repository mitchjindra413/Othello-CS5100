# Agent.py
from signal import alarm

from Board import Board
from enum import Enum
from typing import Tuple
class AgentDifficulty(Enum):
    EASY = 0
    HARD = 1

# The Agent class represents the AI opponent in the Othello game.
class Agent:
    def __init__(self, depth: int, color = False, difficulty = AgentDifficulty.EASY):
        self.color = color  # AI plays as White (False) by default
        self.difficulty = difficulty
        self.board_weights = [
            [100, -20,  10,   5,   5,  10, -20, 100],
            [-20, -50,  -2,  -2,  -2,  -2, -50, -20],
            [ 10,  -2,   5,   1,   1,   5,  -2,  10],
            [  5,  -2,   1,   0,   0,   1,  -2,   5],
            [  5,  -2,   1,   0,   0,   1,  -2,   5],
            [ 10,  -2,   5,   1,   1,   5,  -2,  10],
            [-20, -50,  -2,  -2,  -2,  -2, -50, -20],
            [100, -20,  10,   5,   5,  10, -20, 100]
        ]
        self.depth = depth
    
    def get_best_move(self, board: Board):
        _, move = self._alpha_beta(board, float("-inf"), float("inf"), self.color, self.depth)
        return move
    
    def _alpha_beta(self, board: Board, alpha: int, beta: int, player: bool, round: int) -> Tuple[int, Tuple[int, int]]:
        if round == self.depth or board.check_game_over():
            if self.difficulty == AgentDifficulty.EASY:
                return self._easy_heuristic(board)
            else: return self._hard_heuristic(board)

        moves = board.get_valid_moves(player)
        if not moves:
            eval, _ = self._alpha_beta(board, alpha, beta, not player, round - 1)
            return (eval, None)

        best_move = None
        if player == self.color:
            max_eval = float("-inf")
            for move in moves:
                new_state = board.copy()
                new_state.make_move(move[0], move[1], player)
                eval, _ =  self._alpha_beta(new_state, alpha, beta, not player, round - 1)

                if eval > max_eval: 
                    max_eval = eval
                    best_move = move
                
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return (max_eval, best_move)
        
        else:
            min_eval = float("inf")
            for move in moves:
                new_state = board.copy()
                new_state.make_move(move[0], move[1], player)
                eval, _ = self._alpha_beta(new_state, alpha, beta, not player, round - 1)

                if eval < min_eval:
                    min_eval = eval
                    best_move = move

                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return (min_eval, best_move)
    
    def _easy_heuristic(self, board: Board):
        black_count, white_count =  board.count_pieces()
        if self.color:
            return black_count - white_count
        else:
            return white_count - black_count

    def _hard_heuristic(self, board: Board):
        score = 0
        for row in range(8):
            for col in range(8):
                tile = board[row][col]
                if tile == self.color:
                    score += self.board_weights[row][col]
                elif tile == (not self.color):
                    score -= self.board_weights[row][col]
                    
        return score

