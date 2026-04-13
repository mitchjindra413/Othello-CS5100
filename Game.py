# Game.py
# Othello/Reversi game with a human player and an AI opponent using the Minimax algorithm.  
import Agent
import TerminalUI

# The board is represented as an 8x8 grid, where each cell can be:
# None (empty), True (Black piece), or False (White piece).
# Board representation:
# _ 0_1_2_3_4_5_6_7_
# 0 |. . . . . . . .
# 1 |. . . . . . . .
# 2 |. . . . . . . .
# 3 |. . . W B . . .
# 4 |. . . B W . . .
# 5 |. . . . . . . .
# 6 |. . . . . . . .
# 7 |. . . . . . . .
class Board:
    # Initialize the board with the starting position
    def __init__(self, rows=8, cols=8):
        self.board = [[None for _ in range(cols)] for _ in range(rows)]
        self.board[3][4] = True
        self.board[4][3] = True
        self.board[3][3] = False
        self.board[4][4] = False
        self.num_rows = rows
        self.num_cols = cols

    # Create a deep copy of the board to prevent modifications to the original board during AI calculations
    def copy(self):
        new_board = Board(self.num_rows, self.num_cols)
        new_board.board = [row[:] for row in self.board]  # Deep copy of the board
        return new_board
    
    # Get a list of valid moves for the given color
    def get_valid_moves(self, color):
        valid_moves = []
        # Check each cell on the board to see if it's a valid move for the given color
        # Note: user input is in the format "x y" where x is the column and y is the row, 
        # so we need to check the board in the same way (board[y][x]) to maintain consistency between user input and board representation.
        for x in range(self.num_cols):
            for y in range(self.num_rows):
                # A move is valid if the cell is empty and placing a piece there would flip at least one of the opponent's pieces
                # Note: we need to check if the cell is empty before checking if it's a valid move, 
                # because the is_valid_move function assumes that the cell is empty and will not work correctly if the cell is already occupied.
                if self.board[y][x] is None and self.is_valid_move(x, y, color):
                    valid_moves.append((x, y))
        return valid_moves

    # Check if placing a piece at (x, y) is a valid move for the given color
    def is_valid_move(self, x, y, color):
        # Check in all 8 directions
        directions = self.possible_move_directions()
        
        # A move is valid if there is at least one opponent's piece in a straight line 
        # (in any of the 8 directions) followed by a piece of the player's color
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            found_opponent = False
            
            # Move in the direction until we find a piece of the player's color or an empty cell
            while 0 <= nx < self.num_cols and 0 <= ny < self.num_rows:
                if self.board[ny][nx] is None:
                    found_opponent = False
                    break
                if self.board[ny][nx] == color:
                    if found_opponent:
                        return True
                    break
                found_opponent = True
                nx += dx
                ny += dy
        
        return False
    
    # Make a move and flip the opponent's pieces
    def make_move(self, x, y, color):
        # First, check if the move is valid. If it's not valid, return False.
        if not self.is_valid_move(x, y, color):
            return False
        
        # Place the piece on the board
        # Note: we need to place the piece before flipping the opponent's pieces, 
        # because the flipping logic relies on the presence of the player's piece on the board.
        self.board[y][x] = color
        
        # Flip opponent's pieces
        directions = self.possible_move_directions()
        
        # For each direction, check if there are opponent's pieces to flip. If there are, flip them.
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            pieces_to_flip = []
            
            # Move in the direction until we find a piece of the player's color or an empty cell
            while 0 <= nx < 8 and 0 <= ny < 8:
                # If we find an empty cell, we can't flip any pieces in this direction, so break out of the loop
                if self.board[ny][nx] is None:
                    break
                # If we find a piece of the player's color, we can flip all the opponent's pieces in this direction, so break out of the loop
                if self.board[ny][nx] == color:
                    for px, py in pieces_to_flip:
                        self.board[py][px] = color
                    break
                # If we find an opponent's piece, add it to the list of pieces to flip and continue moving in the same direction
                pieces_to_flip.append((nx, ny))
                nx += dx
                ny += dy
        
        return True
    
    # Utility function to return the possible move directions 
    # (8 directions: N, NE, E, SE, S, SW, W, NW)
    def possible_move_directions(self):
        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1),          (0, 1),
                      (1, -1), (1, 0), (1, 1)]
                      
        return directions
    
    # Count the number of pieces on the board for each player
    def count_pieces(self):
        black_count = sum(row.count(True) for row in self.board)
        white_count = sum(row.count(False) for row in self.board)
        return black_count, white_count


# The Game class manages the game loop and interactions between the human player and the AI opponent.
# The human player will play as Black (True), and the AI will play as White (False).
# The game will continue until neither player has any valid moves left.
class Game:
    # Initialize the game with a board and an agent
    def __init__(self):
        self.ui = TerminalUI.TerminalUI()  # Create an instance of the TerminalUI class for displaying messages and valid moves
        self.board = Board()
        self.agent = Agent.Agent(False)  # AI plays as White (False)

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
                  
            if self.check_game_over():
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

    # Check if the game is over (i.e., neither player has any valid moves left)
    def check_game_over(self):
        # The game is over if neither player has any valid moves left
        return not self.board.get_valid_moves(True) and not self.board.get_valid_moves(False)
    
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