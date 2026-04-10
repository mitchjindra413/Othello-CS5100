import Agent

# White = True
# Black = False
# Board
# _ _ 0 _ 1 _ 2 _ ... 
# 0 |
# 1 |
# 2 |
# ... |

class Game:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.board[3][3] = True
        self.board[4][4] = True
        self.board[3][4] = False
        self.board[4][3] = False

        self.agent = Agent(self.board)