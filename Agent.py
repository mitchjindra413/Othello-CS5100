# Agent.py

# The Agent class represents the AI opponent in the Othello game.
class Agent:
    def __init__(self, board):
        self.board = board
    
    # For testing the game, AI just returns the first valid move for now.
    # TODO: use Minimax algorithm with alpha-beta pruning to find the best move.
    def get_best_move(self, color):
        valid_moves = self.board.get_valid_moves(color)
        if not valid_moves:
            return None
        
        return valid_moves[0]