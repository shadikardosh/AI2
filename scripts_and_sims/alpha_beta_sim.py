from run_game import GameRunner
from players import simple_player, random_player

setup_time = 2
k = 5
time_per_k_turns = 1
res = ""

game1 = GameRunner(setup_time, time_per_k_turns, k, 'n', "alpha_beta_player", "simple_player")
print("alpha_beta_starts:")
for i in range(5):
    res = game1.run()

game2 = GameRunner(setup_time, time_per_k_turns, k, 'n', "simple_player", "alpha_beta_player")
print("simple_player starts:")
for i in range(5):
    game2.run()