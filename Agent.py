# Agent.py

# The Agent class represents the AI opponent in the Othello game.
class Agent:
    def __init__(self, color = False):
        self.color = color  # AI plays as White (False) by default
    
    # For testing the game, AI just returns the first valid move for now.
    # TODO: use Minimax algorithm with alpha-beta pruning to find the best move.
    def get_best_move(self, board):
        valid_moves = board.get_valid_moves(self.color)
        if not valid_moves:
            return None
        
        return valid_moves[0]