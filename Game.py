# Game.py
# Othello/Reversi game with a human player and an AI opponent using the Minimax algorithm.  
from Agent import Agent, AgentDifficulty
from TerminalUI import TerminalUI
from Board import Board
from sys import argv

# The Game class manages the game loop and interactions between the human player and the AI opponent.
# The human player will play as Black (True), and the AI will play as White (False).
# The game will continue until neither player has any valid moves left.
class Game:
    # Initialize the game with a board and an agent
    def __init__(self, player_color = True, depth = 4, difficulty = AgentDifficulty.EASY):
        try:
            from GraphicalUI import GraphicalUI
            self.ui = GraphicalUI()  # Create an instance of the GraphicalUI class for displaying messages and valid moves
        except ModuleNotFoundError:
            self.ui = TerminalUI()  # Fallback to TerminalUI if GraphicalUI is not available
        except Exception as e:
            print(f"Error initializing UI: {e}")
            self.ui = TerminalUI() # Fallback to TerminalUI if there is any error initializing the GraphicalUI
        self.board = Board()
        self.agent = Agent(not player_color, depth, difficulty)  # AI plays as White (False)

    # Print the current state of the board
    def print_board(self):
        self.ui.display_board(self.board)

    # Main game loop
    def play(self):
        current_color = True  # Black starts
        while True:
            self.ui.display_board(self.board)  # Print the board state at the beginning of each turn
            valid_moves = self.board.get_valid_moves(current_color)
            if valid_moves:
                if current_color:  # Human player (Black)
                    move = self.player_move()
                else:  # AI player (White)
                    self.ai_move()  # Pass the board directly; undo/redo prevents modification
            else:
                print(f"{'Black' if current_color else 'White'} has no valid moves.")
                # pass back to other player until both players have no valid moves left, then end the game
         
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
    def ai_move(self):
        move = self.agent.get_best_move(self.board)  # AI plays as White (False)
        print(f"AI selected move: {move}")  # Print the AI's selected move to the console for debugging purposes
        if move:
            self.board.make_move(move[0], move[1], False)
            self.ui.display_move(move, False)  # Display the AI's move in the UI
        else:
            print("AI has no valid moves.")
            # pass back to human player until both players have no valid moves left, then end the game
    
    # If the game is over, print the final score and declare the winner
    def end_game(self):
        # Print the final board state before declaring the winner
        black_score, white_score = self.board.count_pieces()
        self.ui.display_end_game(self.board, black_score, white_score)

if __name__ == "__main__":
    difficulty = AgentDifficulty.EASY
    depth = 4

    if len(argv) == 2:
        arg_difficulty = argv[1].lower()
        match arg_difficulty:
            case "easy":
                difficulty = AgentDifficulty.EASY
            case "hard":
                difficulty = AgentDifficulty.HARD
            case _:
                difficulty = AgentDifficulty.EASY
    if len(argv) == 3:
        depth = int(argv[2])

    print(r"""   ____  _   _          _ _       
  / __ \| | | |        | | |      
 | |  | | |_| |__   ___| | | ___  
 | |  | | __| '_ \ / _ \ | |/ _ \ 
 | |__| | |_| | | |  __/ | | (_) |
  \____/ \__|_| |_|\___|_|_|\___/ 
                                  """)

    print(f"Mode: {difficulty}, Depth: {depth} ")
    game = Game(depth = depth, difficulty = difficulty)
    game.play()