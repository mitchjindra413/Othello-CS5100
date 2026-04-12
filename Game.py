# Game.py
# Othello/Reversi game with a human player and an AI opponent using the Minimax algorithm.  
import Agent

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
                if self.board[x][y] is None and self.is_valid_move(x, y, color):
                    valid_moves.append((x, y))
        return valid_moves
    
    # Utility function to print valid moves to the console
    def print_valid_moves(self, valid_moves):
        joined_moves = ",".join(f"({move[1]} {move[0]})" for move in valid_moves)  # Convert to (y, x) format for user-friendly display
        print("Valid moves: " + joined_moves)

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
            while 0 <= nx < self.num_rows and 0 <= ny < self.num_cols:
                if self.board[nx][ny] is None:
                    found_opponent = False
                    break
                if self.board[nx][ny] == color:
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
        self.board[x][y] = color
        
        # Flip opponent's pieces
        directions = self.possible_move_directions()
        
        # For each direction, check if there are opponent's pieces to flip. If there are, flip them.
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            pieces_to_flip = []
            
            # Move in the direction until we find a piece of the player's color or an empty cell
            while 0 <= nx < 8 and 0 <= ny < 8:
                # If we find an empty cell, we can't flip any pieces in this direction, so break out of the loop
                if self.board[nx][ny] is None:
                    break
                # If we find a piece of the player's color, we can flip all the opponent's pieces in this direction, so break out of the loop
                if self.board[nx][ny] == color:
                    for px, py in pieces_to_flip:
                        self.board[px][py] = color
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
    
    # Print the board state to the console
    def print_board(self):
        print("  _" + "_".join(str(i) for i in range(self.num_cols)) + "_")
        for y in range(self.num_rows):
            piece_symbols = [".", "B", "W"]
            print(f"{y} |" + " ".join(piece_symbols[0] if cell is None else piece_symbols[1] if cell else piece_symbols[2] for cell in self.board[y]))

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
        self.board = Board()
        self.agent = Agent.Agent(self.board)

    # Print the current state of the board
    def print_board(self):
        self.board.print_board()

    # Main game loop
    def play(self):
        current_color = True  # Black starts
        while True:
            self.board.print_board()
            valid_moves = self.board.get_valid_moves(current_color)
            if not valid_moves:
                print(f"{'Black' if current_color else 'White'} has no valid moves.")
                # pass back to AI until both players have no valid moves left, then end the game
            
            if current_color:  # Human player (Black)
                if not self.player_move():
                    continue  # If the player's move was invalid, prompt them to enter a move again
            else:  # AI player (White)
                self.ai_move()
            
            if self.check_game_over():
                self.print_end_game()
                break
            
            current_color = not current_color  # Switch turns

    # Handle the player's move and return True if the move was successful, False otherwise
    def player_move(self):
        move = input("Enter your move (Black) (x y): ")
        try:
            y, x = map(int, move.split())
            if (x, y) not in self.board.get_valid_moves(True):
                print("Invalid move. Please choose a valid move from the list.")
                self.board.print_valid_moves(self.board.get_valid_moves(True))
                return False
            self.board.make_move(x, y, True)
            return True
        except ValueError:
            print("Invalid input format. Please enter two integers separated by a space.")
            self.board.print_valid_moves(self.board.get_valid_moves(True))
            return False
    
    # Handle the AI's move and print it to the console
    def ai_move(self):
        move = self.agent.get_best_move(False)  # AI plays as White (False)
        if move:
            self.board.make_move(move[0], move[1], False)
            print(f"AI plays: ({move[1]} {move[0]})")  # Print move in (y, x) format due to user input format
        else:
            print("AI has no valid moves.")
            # pass back to human player until both players have no valid moves left, then end the game

    # After the game is over, print the final score and declare the winner
    def print_final_score(self):
        black_count, white_count = self.board.count_pieces()
        print(f"Final Score - Black: {black_count}, White: {white_count}")
        if black_count > white_count:
            print("Black wins!")
        elif white_count > black_count:
            print("White wins!")
        else:
            print("It's a tie!")
    
    # Check if the game is over (i.e., neither player has any valid moves left)
    def check_game_over(self):
        # The game is over if neither player has any valid moves left
        return not self.board.get_valid_moves(True) and not self.board.get_valid_moves(False)
    
    # If the game is over, print the final score and declare the winner
    def print_end_game(self):
        # Print the final board state before declaring the winner
        self.board.print_board()
        print("Game over.")
        self.print_final_score()

if __name__ == "__main__":
    game = Game()
    game.play()