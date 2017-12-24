from run_game import GameRunner
from players import simple_player, random_player

setup_time = 2
k = 5
time_per_k_turns = 1
res = ""

game1 = GameRunner(setup_time, time_per_k_turns, k, 'n', "random_player", "simple_player")
print("Random player starts:")
for i in range(3):
    res = game1.run()

game2 = GameRunner(setup_time, time_per_k_turns, k, 'n', "simple_player", "random_player")
print("Simple player starts:")
for i in range(3):
    game2.run()

