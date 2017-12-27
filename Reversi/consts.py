
#==============================================================================
# Game pieces
# - EM is an empty location on the board.
#==============================================================================
EM = ' '

X_PLAYER = 'X'
O_PLAYER = 'O'
TIE = 'tie'

#===============================================================================
# Board Shape
#===============================================================================
BOARD_ROWS = BOARD_COLS = 8

# The Opponent of each Player
OPPONENT_COLOR = {
    X_PLAYER: O_PLAYER,
    O_PLAYER: X_PLAYER
}

translate_moves_dict = {'a': 7, 'b': 6, 'c': 5, 'd': 4, 'e': 3, 'f': 2, 'g': 1, 'h': 0 }