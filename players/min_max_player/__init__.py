#===============================================================================
# Imports
#===============================================================================

import abstract
from players.better_player import Player as BasePlayer
from utils import INFINITY, run_with_limited_time, ExceededTimeError, MiniMaxAlgorithm
from Reversi.consts import EM, OPPONENT_COLOR, BOARD_COLS, BOARD_ROWS
import time
import copy
from collections import defaultdict

#===============================================================================
# Player
#===============================================================================


class Player(BasePlayer):
    def __init__(self, setup_time, player_color, time_per_k_turns, k):
        BasePlayer.__init__(self, setup_time, player_color, time_per_k_turns, k)
        self.board_bonus_factor = 1
        self.max_depth = 10
        self.executed_moves = 0
        self.end_game_threshold = 10
        self.depth = 0

    #def calculateBoardBonus(self, my_bb, op_bb):
     #   if my_bb != op_bb and my_bb != -op_bb:
      #      return self.board_bonus_factor * (my_bb-op_bb)/(my_bb+op_bb)
       # return 0

    def calculateMobilityBonus(self, state):
        if self.no_more_time():
            return 0
        my_mobility, op_mobility = self.__calculateEachPlayersMoves(state)
        if my_mobility != op_mobility:
            return self.mobility_factor*(my_mobility-op_mobility)/(op_mobility+my_mobility)
        return 0

    def utility(self, state):
        if self.executed_moves > self.end_game_threshold:
            self.turnOffExtraHeuristics()
        res = BasePlayer.utility(self, state)
        self.restoreExtraHuerestics()
        return res

    def get_move(self, game_state, possible_moves):
        self.clock = time.time()
        self.time_for_current_move = self.time_remaining_in_round / self.turns_remaining_in_round - 0.05
        if len(possible_moves) == 1:
            return possible_moves[0]

        # best_move = possible_moves[0]
        # next_state = copy.deepcopy(game_state)
        # next_state.perform_move(best_move[0], best_move[1])
        # # Choosing an arbitrary move
        # # Get the best move according the utility function
        # for move in possible_moves:
        #     new_state = copy.deepcopy(game_state)
        #     new_state.perform_move(move[0], move[1])
        #     if self.utility(new_state) > self.utility(next_state):
        #         next_state = new_state
        #         best_move = move
        best_move = possible_moves[0]
        min_max = MiniMaxAlgorithm(self.utility, self.color, self.no_more_time, None)
        self.depth = 1
        while self.no_more_time() is False:
            min_max_val = min_max.search(game_state, self.depth, True)[1]
            best_move = min_max_val if min_max_val is not None else best_move
            self.depth += 1
        if self.turns_remaining_in_round == 1:
            self.turns_remaining_in_round = self.k
            self.time_remaining_in_round = self.time_per_k_turns
        else:
            self.turns_remaining_in_round -= 1
            self.time_remaining_in_round -= (time.time() - self.clock)

        self.executed_moves += 1
        return best_move

    def __repr__(self):
        return '{} {}'.format(abstract.AbstractPlayer.__repr__(self), 'minimax')