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
    
    # Provides best move available to AI player using Alpha Beta Pruning
    def get_best_move(self, board: Board):
        _, move = self._alpha_beta(board, float("-inf"), float("inf"), self.color, self.depth)
        return move
    
    # Alpha Beta Pruning algorithm to evaluate the game tree and find the best move for the AI player
    def _alpha_beta(self, board: Board, alpha: int, beta: int, player: bool, round: int) -> Tuple[int, Tuple[int, int]]:
        # If we've reached the maximum depth or the game is over, evaluate the board state using the appropriate heuristic function based on the difficulty level
        if round == self.depth or board.check_game_over():
            if self.difficulty == AgentDifficulty.EASY:
                return (self._easy_heuristic(board), None)
            else: 
                return (self._hard_heuristic(board), None)

        moves = board.get_valid_moves(player)
        # If there are no valid moves for the current player, we need to pass the turn to the opponent and continue searching the game tree
        if not moves:
            eval, _ = self._alpha_beta(board, alpha, beta, not player, round - 1)
            return (eval, None)

        best_move = None
        # If the current player is the AI player, we want to maximize the evaluation score, so we initialize max_eval to negative infinity and update it whenever we find a better move
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
                # If beta is less than or equal to alpha, we can stop searching the rest of the moves at this level because we know that the opponent will not allow us to reach better states
                if beta <= alpha:
                    break
            return (max_eval, best_move)
        
        # If the current player is the opponent, we want to minimize the evaluation score for the AI player, so we initialize min_eval to positive infinity and update it whenever we find a worse move for the AI player
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
                # If beta is less than or equal to alpha, we can stop searching the rest of the moves at this level because we know that the opponent will not allow us to reach better states
                if beta <= alpha:
                    break
            return (min_eval, best_move)
    
    # The easy heuristic function counts the number of pieces for each player and returns the difference, 
    # The AI player has positive score if they have more pieces and a negative score if the opponent has more pieces
    def _easy_heuristic(self, board: Board):
        black_count, white_count =  board.count_pieces()
        if self.color:
            return black_count - white_count
        else:
            return white_count - black_count

    # The hard heuristic function uses a weighted evaluation of the board state, where each position on the board has a different weight based on its strategic importance
    # The AI player gets a positive score for occupying high-weight positions and a negative score for occupying low-weight positions, while the opponent gets the opposite
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

