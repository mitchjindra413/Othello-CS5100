# Board.py
# The board is an 8x8 grid, where each cell can be:
# None (empty), True (player piece), or False (AI piece).
# It is used by the Game class and the Agent class.

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
            while 0 <= ny < self.num_rows and 0 <= nx < self.num_cols:
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

    # Check if the game is over (i.e., neither player has any valid moves left)
    def check_game_over(self):
        # The game is over if neither player has any valid moves left
        return not self.get_valid_moves(True) and not self.get_valid_moves(False)