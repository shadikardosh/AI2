#===============================================================================
# Imports
#===============================================================================

import abstract
from players.better_player import Player as BasePlayer

#===============================================================================
# Player
#===============================================================================


class Player(BasePlayer):
    def __init__(self, setup_time, player_color, time_per_k_turns, k):
        BasePlayer.__init__(self, setup_time, player_color, time_per_k_turns, k)

        # board map bonus
        # Based on Washington University research
        self.corner_bonus = 4
        self.board_bonus = [[self.corner_bonus, -3, 2 , 2 , 2 , 2 , -3, self.corner_bonus],
                            [-3, -4, -1, -1, -1, -1, -4, -3],
                            [2 , -1, 1 , 0 , 0 , 1 , -1, 2],
                            [2 , -1, 0 , 1 , 1 , 0 , -1, 2],
                            [2 , -1, 0 , 1 , 1 , 0 , -1, 2],
                            [2 , -1, 1 , 0 , 0 , 1 , -1, 2],
                            [-3, -4, -1, -1, -1, -1, -4, -3],
                            [self.corner_bonus, -3, 2 , 2 , 2 , 2 , -3, self.corner_bonus]]

    def deepUpdateBoardBonus(self, state):
        return self.updateBoardBonus(state)

    def __repr__(self):
        return '{} {}'.format(abstract.AbstractPlayer.__repr__(self), 'b1')