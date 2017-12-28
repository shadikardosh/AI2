
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
game_book = ['+d3-c5+f6-f5+e6-e3+c3-f3+c4-b4 ',
                '+d3-c5+f6-e3+c3-f5+e6-f3+c4-b4 ',
                '+d3-c5+e6-f5+f6-e3+c3-f3+c4-b4 ',
                '+d3-c5+f6-f5+e6-e3+d6-f7+g6-e7 ',
                '+d3-c5+e6-f5+f6-e3+d6-f7+g6-e7 ',
                '+d3-c5+f6-f5+e6-e3+c3-d2+c4-b5 ',
                '+d3-c5+f6-e3+c3-f5+e6-d2+c4-b5 ',
                '+d3-c5+e6-f5+f6-e3+c3-d2+c4-b5 ',
                '+d3-c5+d6-e3+f4-c6+f5-c3+c4-b5 ',
                '+d3-c3+c4-e3+d2-c5+b3-e2+f3-d1 ',
                '+d3-c5+f6-f5+e6-e3+d6-f7+g6-f4 ',
                '+d3-c5+e6-f5+f6-e3+d6-f7+g6-f4 ',
                '+d3-c5+f6-f5+e6-e3+d6-f7+g6-c3 ',
                '+d3-c5+e6-f5+f6-e3+d6-f7+g6-c3 ',
                '+d3-c3+c4-e3+d2-c5+b5-b4+f3-f2 ',
                '+d3-c3+c4-e3+d2-b4+b5-c5+f3-f2 ',
                '+d3-c3+c4-e3+d2-b4+f4-c2+c5-e6 ',
                '+d3-c3+c4-e3+d2-c5+b4-c2+d6-e6 ',
                '+d3-c3+c4-e3+d2-c5+b4-b3+f4-f5 ',
                '+d3-c3+c4-e3+d2-c2+b4-c5+d6-e6 ',
                '+d3-c3+c4-e3+d2-b4+f4-c2+f5-d6 ',
                '+d3-c3+c4-e3+f4-d6+e6-b4+c6-g4 ',
                '+d3-c5+f6-f5+e6-e3+d6-f7+g6-c4 ',
                '+d3-c5+e6-f5+f6-e3+d6-f7+g6-c4 ',
                '+d3-c5+f6-f5+e6-e3+c3-d2+c4-b3 ',
                '+d3-c5+f6-e3+c3-f5+e6-d2+c4-b3 ',
                '+d3-c5+e6-f5+f6-e3+c3-d2+c4-b3 ',
                '+d3-c3+c4-e3+d2-c5+b5-b4+f3-e2 ',
                '+d3-c3+c4-e3+d2-b4+b5-c5+f3-e2 ',
                '+d3-c3+c4-e3+f4-c5+e2-f5+f6-f1 ',
                '+d3-c5+d6-e3+f4-c6+c4-c3+e2-f2 ',
                '+d3-c5+f6-f5+e6-e3+c3-d2+c4-d6 ',
                '+d3-c5+f6-e3+c3-f5+e6-d2+c4-d6 ',
                '+d3-c5+e6-f5+f6-e3+c3-d2+c4-d6 ',
                '+d3-c5+f6-f5+e6-e3+c3-d2+f4-f3 ',
                '+d3-c5+f6-e3+c3-f5+e6-d2+f4-f3 ',
                '+d3-c5+e6-f5+f6-e3+c3-d2+f4-f3 ',
                '+d3-c3+c4-e3+f4-d6+c6-c5+b4-b5 ',
                '+d3-c3+c4-e3+f4-c5+c6-d6+b4-b5 ',
                '+d3-c3+c4-e3+d2-b4+f4-f3+f5-c1 ',
                '+d3-c3+c4-e3+d2-c2+e2-b4+f3-f1 ',
                '+d3-c3+c4-e3+d2-b4+f4-c2+f5-c6 ',
                '+d3-c3+c4-e3+d2-c2+e2-b4+f3-d1 ',
                '+d3-c5+f6-f5+e6-e3+c3-f3+f4-e7 ',
                '+d3-c5+f6-e3+c3-f5+e6-f3+f4-e7 ',
                '+d3-c5+e6-f5+f6-e3+c3-f3+f4-e7 ',
                '+d3-c3+c4-e3+f4-c5+e2-f5+f6-g5 ',
                '+d3-c3+c4-e3+f4-c5+e6-f3+f2-f6 ',
                '+d3-e3+f4-c3+f5-g4+f3-g3+c4-g5 ',
                '+d3-c3+c4-e3+f4-c5+e6-g4+b3-c6 ',
                '+d3-c3+c4-e3+f4-d6+e6-b5+c6-g5 ',
                '+d3-c3+c4-e3+d2-c5+b5-b4+f3-c2 ',
                '+d3-c3+c4-e3+d2-b4+b5-c5+f3-c2 ',
                '+d3-c3+c4-e3+c2-c5+f4-f3+e2-d2 ',
                '+d3-c3+c4-e3+f4-d6+d2-f2+c6-c5 ',
                '+d3-c3+c4-e3+d2-c5+b4-c2+d6-e2 ',
                '+d3-c3+c4-e3+d2-c5+b4-b3+f4-b5 ',
                '+d3-c3+c4-e3+d2-c2+b4-c5+d6-e2 ',
                '+d3-c3+c4-e3+d2-b4+f4-f3+f5-f6 ',
                '+d3-c3+c4-e3+f4-c5+e6-g4+b5-c6 ',
                '+d3-c3+c4-e3+f4-d6+e6-b5+c6-g4 ',
                '+d3-c5+f6-f5+e6-e3+c3-f3+e2-d2 ',
                '+d3-c5+f6-e3+c3-f5+e6-f3+e2-d2 ',
                '+d3-c5+e6-f5+f6-e3+c3-f3+e2-d2 ',
                '+d3-c3+c4-e3+d2-c2+b4-d1+f4-b3 ',
                '+d3-c3+c4-e3+f4-c5+e2-f5+b6-c6 ',
                '+d3-c3+c4-e3+d2-c5+f5-f4+d6-c6 ',
                '+d3-c3+c4-e3+d2-c5+b5-b4+d6-e6 ',
                '+d3-c3+c4-e3+d2-b4+b5-c5+d6-e6 ']
