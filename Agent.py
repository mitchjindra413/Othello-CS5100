# Agent.py
from Board import Board
from enum import Enum
from typing import Tuple
class AgentDifficulty(Enum):
    EASY = 0
    HARD = 1
    EXPERT = 2

# The Agent class represents the AI opponent in the Othello game.
class Agent:
    def __init__(self, color = False, depth: int = 6, difficulty = AgentDifficulty.EASY):
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
        if round == 0 or board.check_game_over():
            if self.difficulty == AgentDifficulty.EASY:
                return (self._easy_heuristic(board), None)
            elif self.difficulty == AgentDifficulty.HARD: 
                return (self._hard_heuristic(board), None)
            else:
                return (self._expert_heuristic(board), None)

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
                move_record = board.make_move(move[0], move[1], player)
                eval, _ =  self._alpha_beta(board, alpha, beta, not player, round - 1)
                board.undo_move(move_record)

                if eval > max_eval: 
                    max_eval = eval
                    best_move = move

                if eval > beta:
                    return (eval, best_move)
                alpha = max(alpha, eval)
            return (max_eval, best_move)
        
        # If the current player is the opponent, we want to minimize the evaluation score for the AI player, so we initialize min_eval to positive infinity and update it whenever we find a worse move for the AI player
        else:
            min_eval = float("inf")
            for move in moves:
                move_record = board.make_move(move[0], move[1], player)
                eval, _ = self._alpha_beta(board, alpha, beta, not player, round - 1)
                board.undo_move(move_record)

                if eval < min_eval:
                    min_eval = eval
                    best_move = move

                if eval < alpha:
                    return (min_eval, best_move)
                beta = min(beta, eval)
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
        for y in range(8):
            for x in range(8):
                tile = board.board[y][x]
                if tile == self.color:
                    score += self.board_weights[y][x]
                elif tile == (not self.color):
                    score -= self.board_weights[y][x]
                    
        return score
    
    def _expert_heuristic(self, board: Board):
        # Modified from example: https://kartikkukreja.wordpress.com/2013/03/30/heuristic-function-for-reversiothello/
        opponent_color = not self.color
        
        # 1. Positional Score (Static Weights)
        score = self._hard_heuristic(board)
        
        # 2. Mobility (Number of legal moves)
        # Having more options is critical in the mid-game
        p_moves = len(board.get_valid_moves(self.color))
        o_moves = len(board.get_valid_moves(opponent_color))
        
        if p_moves + o_moves != 0:
            mobility = 100 * (p_moves - o_moves) / (p_moves + o_moves)
        else:
            mobility = 0

        # 3. Corner Occupancy
        # Corners are stable and cannot be flipped back
        p_corners = 0
        o_corners = 0
        corners = [(0,0), (0,7), (7,0), (7,7)]
        for x, y in corners:
            if board.board[y][x] == self.color:
                p_corners += 1
            elif board.board[y][x] == opponent_color:
                o_corners += 1
        
        if p_corners + o_corners != 0:
            corner_score = 100 * (p_corners - o_corners) / (p_corners + o_corners)
        else:
            corner_score = 0

        # 4. Tile Count
        # Should only impact late game decision making processes
        black_count, white_count = board.count_pieces()
        p_count = black_count if self.color else white_count
        o_count = white_count if self.color else black_count
        
        tile_score = 0
        total_pieces = p_count + o_count
        
        if total_pieces > 50:
            tile_score = 100 * (p_count - o_count) / total_pieces

        # 5. Final Weighted Combination
        return (score) + (15 * mobility) + (25 * corner_score) + (10 * tile_score)