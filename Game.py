# Game.py
# Othello/Reversi game with a human player and an AI opponent using the Minimax algorithm.  
from Agent import Agent
import TerminalUI
from Board import Board


# The Game class manages the game loop and interactions between the human player and the AI opponent.
# The human player will play as Black (True), and the AI will play as White (False).
# The game will continue until neither player has any valid moves left.
class Game:
    # Initialize the game with a board and an agent
    def __init__(self):
        self.ui = TerminalUI.TerminalUI()  # Create an instance of the TerminalUI class for displaying messages and valid moves
        self.board = Board()
        self.agent = Agent(False)  # AI plays as White (False)

    # Print the current state of the board
    def print_board(self):
        self.ui.display_board(self.board)

    # Main game loop
    def play(self):
        current_color = True  # Black starts
        while True:
            self.ui.display_board(self.board)  # Print the board state at the beginning of each turn
            valid_moves = self.board.get_valid_moves(current_color)
            if not valid_moves:
                print(f"{'Black' if current_color else 'White'} has no valid moves.")
                # pass back to AI until both players have no valid moves left, then end the game

            if current_color:  # Human player (Black)
                move = self.player_move()

            else:  # AI player (White)
                self.ai_move(self.board.copy()) # Pass a copy of the board to the AI to prevent it from modifying the actual game board during its calculations
                  
            if self.board.check_game_over():
                self.end_game()
                break
            
            current_color = not current_color  # Switch turns
            

    # Handle the player's move
    def player_move(self):
        x, y = self.ui.get_player_input(self.board)
        self.board.make_move(x, y, True)  # Player is always Black (True)
        self.ui.display_move((x, y), True)  # Display the player's move in the UI
    
    # Handle the AI's move
    def ai_move(self, board):
        move = self.agent.get_best_move(board.copy())  # AI plays as White (False)
        if move:
            self.board.make_move(move[0], move[1], False)
            self.ui.display_move(move, False)  # Display the AI's move in the UI
        else:
            print("AI has no valid moves.")
            # pass back to human player until both players have no valid moves left, then end the game
    
    # If the game is over, print the final score and declare the winner
    def end_game(self):
        # Print the final board state before declaring the winner
        self.ui.display_board(self.board)
        self.ui.display_message("Game over.")
        black_score, white_score = self.board.count_pieces()
        self.ui.display_score(black_score, white_score)
        self.ui.display_winner(black_score, white_score)

if __name__ == "__main__":
    game = Game()
    game.play()