# TerminalUI.py
# A view class for displaying the game board and messages in the terminal,
# as well as getting input from the player.
# It is used by the Game class.

class TerminalUI:
    # Print the board state to the console
    def display_board(self, board):
        print("  _" + "_".join(str(i) for i in range(board.num_cols)) + "_")
        for y in range(board.num_rows):
            piece_symbols = [".", "B", "W"]
            print(f"{y} |" + " ".join(piece_symbols[0] if cell is None else piece_symbols[1] if cell else piece_symbols[2] for cell in board.board[y]))

    # Display a message to the player in the terminal
    def display_message(self, message):
        print(message)
    
    # Display the current score in the terminal
    def display_score(self, black_score, white_score):
        print(f"Score - Black: {black_score}, White: {white_score}")

    # Declare the winner (at the end of the game)
    def display_winner(self, black_score, white_score):
        if black_score > white_score:
            print("Black wins!")
        elif white_score > black_score:
            print("White wins!")
        else:
            print("It's a tie!")

    # Display the move made by the player or AI in the terminal
    def display_move(self, move, color):
        print(f"{'Black' if color else 'White'} move: ({move[1]} {move[0]})")  # Print move in (y, x) format due to user input format

    # Get the player's move input from the terminal and validate it against the list of valid moves for the player.
    def get_player_input(self, board):
        found_valid_move = False
        while not found_valid_move:
            move = input("Enter your move (Black) (x y): ")
            try:
                y, x = map(int, move.split())
                if (x, y) not in board.get_valid_moves(True):
                    print("Invalid move.")
                    self.print_valid_moves(board, True)
                else:
                    found_valid_move = True
                    return (x, y)
            except ValueError:
                print("Invalid input format. Please enter two integers separated by a space.")
                self.print_valid_moves(board, True)

    # Utility function to print valid moves to the console
    def print_valid_moves(self, board, color=True):
        valid_moves = board.get_valid_moves(color)  # Get valid moves for the player (Black) by default
        joined_moves = ",".join(f"({move[1]} {move[0]})" for move in valid_moves)  # Convert to (y, x) format for user-friendly display
        print("Valid moves: " + joined_moves)