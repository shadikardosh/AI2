#===============================================================================
# Imports
#===============================================================================

import abstract
from utils import INFINITY, run_with_limited_time, ExceededTimeError
from Reversi.consts import EM, OPPONENT_COLOR, BOARD_COLS, BOARD_ROWS
import time
import copy
from collections import defaultdict

#===============================================================================
# Player
#===============================================================================


class Player(abstract.AbstractPlayer):
    def __init__(self, setup_time, player_color, time_per_k_turns, k):
        abstract.AbstractPlayer.__init__(self, setup_time, player_color, time_per_k_turns, k)
        self.clock = time.time()

        # We are simply providing (remaining time / remaining turns) for each turn in round.
        # Taking a spare time of 0.05 seconds.
        self.turns_remaining_in_round = self.k
        self.time_remaining_in_round = self.time_per_k_turns
        self.time_for_current_move = self.time_remaining_in_round / self.turns_remaining_in_round - 0.05

        ############################
        # Heuristics  Helper  Vars #
        ############################
        #sets of my and my oponent's stable cells
        self.my_stables = set()
        self.op_stables = set()
        self.my_max_new_stables = set()
        self.my_max_new_stables = set()

        # board map bonus
        # Based on Washington University research
        self.board_bonus = [[10, -3, 2 , 2 , 2 , 2 , -3, 10],
                            [-3, -4, -1, -1, -1, -1, -4, -3],
                            [2 , -1, 1 , 0 , 0 , 1 , -1, 2],
                            [2 , -1, 0 , 1 , 1 , 0 , -1, 2],
                            [2 , -1, 0 , 1 , 1 , 0 , -1, 2],
                            [2 , -1, 1 , 0 , 0 , 1 , -1, 2],
                            [-3, -4, -1, -1, -1, -1, -4, -3],
                            [10, -3, 2 , 2 , 2 , 2 , -3, 10]]

    def get_move(self, game_state, possible_moves):
        self.clock = time.time()
        self.time_for_current_move = self.time_remaining_in_round / self.turns_remaining_in_round - 0.05
        if len(possible_moves) == 1:
            return possible_moves[0]

        best_move = possible_moves[0]
        next_state = copy.deepcopy(game_state)
        next_state.perform_move(best_move[0], best_move[1])
        # Choosing an arbitrary move
        # Get the best move according the utility function
        for move in possible_moves:
            new_state = copy.deepcopy(game_state)
            new_state.perform_move(move[0], move[1])
            if self.utility(new_state) > self.utility(next_state):
                next_state = new_state
                best_move = move

        if self.turns_remaining_in_round == 1:
            self.turns_remaining_in_round = self.k
            self.time_remaining_in_round = self.time_per_k_turns
        else:
            self.turns_remaining_in_round -= 1
            self.time_remaining_in_round -= (time.time() - self.clock)

        return best_move

    def utility(self, state):
        if len(state.get_possible_moves()) == 0:
            return INFINITY if state.curr_player != self.color else -INFINITY

        STABLE_VAL = BOARD_COLS

        my_cells = 0
        op_cells = 0
        my_u = 0
        op_u = 0
        my_new_stables = set()
        op_new_stables = set()
        for x in range(BOARD_COLS):
            for y in range(BOARD_ROWS):
                if state.board[x][y] == self.color:
                    my_cells += 1
                    my_u += self.board_bonus[x][y]
                    #if self.canBeMyStable(state, (x, y)) and not (x, y) in self.my_stables:
                    #    my_new_stables.add((x, y))
                if state.board[x][y] == OPPONENT_COLOR[self.color]:
                    op_cells += 1
                    op_u += self.board_bonus[x][y]
                    #if self.canBeOpStable(state, (x, y)) and not (x, y) in self.op_stables:
                    #    op_new_stables.add((x, y))

        if my_u == 0:
            # I have no tools left
            return -INFINITY
        elif op_u == 0:
            # The opponent has no tools left
            return INFINITY
        else:
            return my_u - op_u + my_cells - op_cells

    def is_my_stable(self, state, coords):
        return coords in self.my_stables or not state.isOnBoard(coords[0], coords[1])

    def is_op_stable(self, state, coords):
        return coords in self.op_stables or not state.isOnBoard(coords[0], coords[1])

    def is_stable(self, state, coords, isOp):
        if isOp:
            return self.is_op_stable(state, coords)
        return self.is_my_stable(state, coords)

    def canBeVerStable(self, state, coords, isOp):
        x, y = coords
        return self.is_stable(state, (x-1, y), isOp) or self.is_stable(state, (x+1, y), isOp)

    def canBeHorStable(self, state, coords, isOp):
        x, y = coords
        return self.is_stable(state, (x, y-1), isOp) or self.is_stable(state, (x, y+1), isOp)

    def canBeDiagStable(self, state, coords, isOp):
        x, y = coords
        return (self.is_stable(state, (x-1, y-1), isOp) or self.is_stable(state, (x+1, y+1), isOp)) and \
               (self.is_stable(state, (x-1, y+1), isOp) or self.is_stable(state, (x+1, y-1), isOp))

    def canBeStable(self, state, coords, isOp):
        # this implementation does not promise to include all of the stable cells
        # UNLESS the cells are checked in certain order
        # (certain order = BFS order from all of the corners)
        if self.is_stable(state, coords, isOp) and self.canBeHorStable(state, coords, isOp) and \
                self.canBeVerStable(state, coords, isOp) and self.canBeDiagStable(state, coords, isOp):
            return True
        return False

    # How to use:
    # in the utility function, calculate newly added stables for each player
    # in the end, when you decide which move to make,  add them to the suitable stable set
    #
    #                    if self.canBeMyStable(state, (x, y)) and not (x, y) in self.my_stables:
    #                        my_new_stables.add((x, y))
    #
    #                    if self.canBeOpStable(state, (x, y)) and not (x, y) in self.op_stables:
    #                        op_new_stables.add((x, y))

    def canBeMyStable(self, state, coords):
        return self.canBeStable(state, coords, False)

    def canBeOpStable(self, state, coords):
        return self.canBeStable(state, coords, True)

    def selective_deepening_criterion(self, state):
        # Simple player does not selectively deepen into certain nodes.
        return False

    def no_more_time(self):
        return (time.time() - self.clock) >= self.time_for_current_move

    def __repr__(self):
        return '{} {}'.format(abstract.AbstractPlayer.__repr__(self), 'better')