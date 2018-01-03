#===============================================================================
# Imports
#===============================================================================
import re
import abstract
from utils import INFINITY, run_with_limited_time, ExceededTimeError
from Reversi.consts import EM, OPPONENT_COLOR, BOARD_COLS, BOARD_ROWS, translate_moves_dict
import time
import copy
import os
from collections import defaultdict

#===============================================================================
# Player
#===============================================================================
global_conf_id = 0
def setStaticConf(i):
    global_conf_id = i

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

        # Based on Washington University research
        self.confs = [(4, 10, 10, 1),
                      (10, 100, 100, 1),
                      (10, 100, 10, 2),
                      (10, 10, 100, 1),
                      (4, 1, 1, 1),
                      (4, 100, 100, 1),
                      (4, 100, 10, 2),
                      (4, 10, 100, 1),
                      (4, 4, 2, 1.5),
                      (14, 4, 2.5, 2),
                      (14, 10, 10, 100),
                      (9, 4, 2.5, 2),
                      (4, 0, 0, 0)] # this must remain as the last confs!!
        self.corner_bonus, \
            self.mobility_factor, \
            self.stability_bonus_factor, \
            self.board_bonus_factor \
            = self.confs[global_conf_id]
        self.curr_conf = global_conf_id
        self.board_bonus = [[self.corner_bonus, -3, 2 , 2 , 2 , 2 , -3, self.corner_bonus],
                            [-3, -4, -1, -1, -1, -1, -4, -3],
                            [2 , -1, 1 , 0 , 0 , 1 , -1, 2],
                            [2 , -1, 0 , 1 , 1 , 0 , -1, 2],
                            [2 , -1, 0 , 1 , 1 , 0 , -1, 2],
                            [2 , -1, 1 , 0 , 0 , 1 , -1, 2],
                            [-3, -4, -1, -1, -1, -1, -4, -3],
                            [self.corner_bonus, -3, 2 , 2 , 2 , 2 , -3, self.corner_bonus]]

        # helper fields to pass arguments between methods
        self.curr_my_cells = 0
        self.curr_op_cells = 0

        self._curr_prefix = []
        self._op_moves = []
        self._previous_state = None

        self.opening_moves = self._init_most_popular_moves()

    def turnOffExtraHeuristics(self):
        self.setConfig(len(self.confs)-1)

    def restoreExtraHuerestics(self):
        self.setConfig(self.curr_conf)

    def setConfig(self, conf_id): # 2 is agressive, 3 is stable
        self.corner_bonus, \
            self.mobility_factor, \
            self.stability_bonus_factor, \
            self.board_bonus_factor \
            = self.confs[conf_id]

    def numOfConf(self):
        return len(self.confs)

    def get_move(self, game_state, possible_moves):
        for move in self._op_moves:
            prev_state = copy.deepcopy(self._previous_state)
            prev_state.perform_move(move[0], move[1])
            possible_board = prev_state.board
            if possible_board == game_state.board:
                self._curr_prefix.append(move)
                break

        self.clock = time.time()
        self.time_for_current_move = self.time_remaining_in_round / self.turns_remaining_in_round - 0.05
        if len(possible_moves) == 1:
            return possible_moves[0]
        popular_game = self._dejavu() if len(self._curr_prefix) <=10 else None
        if popular_game is not None:
            best_move = self._get_next_popular_move(popular_game)
            new_state = copy.deepcopy(game_state)
            new_state.perform_move(best_move[0], best_move[1])
            self._curr_prefix.append(best_move)
            self._previous_state = copy.deepcopy(new_state)
            new_state.curr_player = OPPONENT_COLOR[self.color]
            self._op_moves = new_state.get_possible_moves()

            self._update_remaining_time()

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

        self._curr_prefix.append(best_move)
        self._previous_state = copy.deepcopy(new_state)
        new_state.curr_player = OPPONENT_COLOR[self.color]
        self._op_moves = new_state.get_possible_moves()

        self._update_remaining_time()

        return best_move

    def utility(self, state):

        my_cells = 0
        op_cells = 0
        my_board_bonus = 0
        op_board_bonus = 0

        #self.updateBoardBonus(state)
        for x in range(BOARD_COLS):
            for y in range(BOARD_ROWS):
                if state.board[x][y] == self.color:
                    my_cells += 1
                    my_board_bonus += self.board_bonus[x][y]
                    #if self.canBeMyStable(state, (x, y)) and not (x, y) in self.my_stables:
                    #    my_new_stables.add((x, y))
                if state.board[x][y] == OPPONENT_COLOR[self.color]:
                    op_cells += 1
                    op_board_bonus += self.board_bonus[x][y]
                    #if self.canBeOpStable(state, (x, y)) and not (x, y) in self.op_stables:
                    #    op_new_stables.add((x, y))

        if my_cells == 0:
            return -INFINITY
        elif op_cells == 0:
            return INFINITY
        else:
            self.curr_my_cells, self.curr_op_cells = my_cells, op_cells
            total_mobility_bonus = self.calculateMobilityBonus(state)
            total_board_bonus = self.calculateBoardBonus(my_board_bonus, op_board_bonus)
            total_stability_bonus = self.calculateStabilityBonus(state)
            return my_cells - op_cells \
                + total_mobility_bonus \
                + total_board_bonus \
                + total_stability_bonus

    def _update_remaining_time(self):
        if self.turns_remaining_in_round == 1:
            self.turns_remaining_in_round = self.k
            self.time_remaining_in_round = self.time_per_k_turns
        else:
            self.turns_remaining_in_round -= 1
            self.time_remaining_in_round -= (time.time() - self.clock)

    def noMoreMovesEvaluation(self, my_cells, op_cells):
        if my_cells > op_cells:
            return INFINITY
        elif my_cells < op_cells:
            return -INFINITY
        else:
            return 0

    def calculateMobilityBonus(self, state):
        if self.mobility_factor == 0:
            return 0
        my_mobility, op_mobility = self.__calculateEachPlayersMoves(state)
        if my_mobility == 0 or op_mobility == 0:
            return self.noMoreMovesEvaluation(self.curr_my_cells, self.curr_op_cells)
        if my_mobility != op_mobility:
            return self.mobility_factor*(my_mobility-op_mobility)/(op_mobility+my_mobility)
        return 0

    def __calculateEachPlayersMoves(self, state):
        state.curr_player = OPPONENT_COLOR[self.color]
        op_possible_moves = state.get_possible_moves()
        op_mobility = len(op_possible_moves)
        # little trick to calculate my_mobility
        state.curr_player = self.color
        my_mobility = len(state.get_possible_moves())
        # return the state.color to what it used to be
        state.curr_player = OPPONENT_COLOR[self.color]
        return my_mobility, op_mobility

    def calculateBoardBonus(self, my_bb, op_bb):
        if self.board_bonus_factor == 0:
            return 0
        if my_bb != op_bb:
            return self.board_bonus_factor * (my_bb-op_bb)
        return 0

    def updateBoardBonus(self, state):
        # call when we have captured x,y
        corner_val = self.corner_bonus
        if state.board[0][0] == self.color:
            self.board_bonus[1][0] = corner_val
            self.board_bonus[0][1] = corner_val
            self.board_bonus[1][1] = 0
        else:
            self.board_bonus[1][0] = -3
            self.board_bonus[0][1] = -3
            self.board_bonus[1][1] = -4

        if state.board[7][0] == self.color:
            self.board_bonus[6][0] = corner_val
            self.board_bonus[7][1] = corner_val
            self.board_bonus[6][1] = 0
        else:
            self.board_bonus[6][0] = -3
            self.board_bonus[7][1] = -3
            self.board_bonus[6][1] = -4

        if state.board[7][7] == self.color:
            self.board_bonus[6][7] = corner_val
            self.board_bonus[7][6] = corner_val
            self.board_bonus[6][6] = 0
        else:
            self.board_bonus[6][7] = -3
            self.board_bonus[7][6] = -3
            self.board_bonus[6][6] = -4

        if state.board[0][7] == self.color:
            self.board_bonus[1][7] = corner_val
            self.board_bonus[0][6] = corner_val
            self.board_bonus[1][6] = 0
        else:
            self.board_bonus[1][7] = -3
            self.board_bonus[0][6] = -3
            self.board_bonus[1][6] = -4

    def calculateStabilityBonus(self, state):
        if self.stability_bonus_factor == 0:
            return 0
        if self.no_more_time():
            return 0

        self.my_stables.clear()
        self.op_stables.clear()

        for i in range(7):
            for j in range(7):
                if self.canBeMyStable(state, (i, j)):
                    self.my_stables.add((i, j))
                if self.canBeMyStable(state, (7-i, j)):
                    self.my_stables.add((7-i, j))
                if self.canBeMyStable(state, (i, 7-j)):
                    self.my_stables.add((i, 7-j))
                if self.canBeMyStable(state, (7-i, 7-j)):
                    self.my_stables.add((7-i, 7-j))

                if self.canBeOpStable(state, (i, j)):
                    self.op_stables.add((i, j))
                if self.canBeOpStable(state, (7-i, j)):
                    self.op_stables.add((7-i, j))
                if self.canBeOpStable(state, (i, 7-j)):
                    self.op_stables.add((i, 7-j))
                if self.canBeOpStable(state, (7-i, 7-j)):
                    self.op_stables.add((7-i, 7-j))

        my_stability = len(self.my_stables)
        op_stability = len(self.op_stables)

        return self.stability_bonus_factor * (my_stability-op_stability)/(my_stability+op_stability)

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
        if self.is_stable(state, coords, isOp) or (self.canBeHorStable(state, coords, isOp) and \
                    self.canBeVerStable(state, coords, isOp) and self.canBeDiagStable(state, coords, isOp)):
            return True
        return False


    def canBeMyStable(self, state, coords):
        return state.board[coords[0]][coords[1]] == self.color and self.canBeStable(state, coords, False)

    def canBeOpStable(self, state, coords):
        return self.canBeStable(state, coords, True)  # missing condition

    def selective_deepening_criterion(self, state):
        # Simple player does not selectively deepen into certain nodes.
        return False

    def no_more_time(self):
        return (time.time() - self.clock) >= self.time_for_current_move

    def __repr__(self):
        return '{} {}'.format(abstract.AbstractPlayer.__repr__(self), 'better')

    def _parse_book(self, book, i):
        '''
        :param fuck: a string describing some game
        :param i: index if a move
        :return: the move as a tuple of (x,y)
        :note: zero indexed
        :note if the string is +d3-a2+b4... then the first move is d3, the second is a2 and the third is b4 (again, zero indexed)
        '''
        if i > 10:
            return None
        x = translate_moves_dict[book[3*i+1]]
        y = int(book[3*i+2])-1
        return x, y

    def _get_first_i_moves(self, i, game):
        '''
        :param i: num of moves required
        :param game: the game itself, as a string
        :return: a list containing the first i moves parsed from the game string
        '''
        res =[]
        for (idx,letter) in enumerate(game):
            if idx >= i:
                break
            res.append(self._parse_book(game, idx))
        return res

    def _dejavu(self):
        '''
        :return: True if the self_curr_prefix is the same as one of the game starts from the game book
        '''
        for game in self.opening_moves:
            prefix = self._get_first_i_moves(len(self._curr_prefix), game)
            if prefix == self._curr_prefix:
                return game
        return None

    def _get_next_popular_move(self, game):
        idx = len(self._curr_prefix)
        return self._get_first_i_moves(idx+1,game)[idx]

    def _init_most_popular_moves(self):
        os.system( 'cut -f1-6 -d"+" ../Reversi/book.gam | sort | uniq -c | sort -rn | cut -f2-10 -d" "| cut -f2-10 -d" " | head -70 > opening_moves.txt')
        with open('opening_moves.txt') as moves:
            content = moves.readlines()
        content = [x.strip() for x in content]
        os.system('rm -f opening_moves.txt')
        return content


