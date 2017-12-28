
from run_game import GameRunner

setup_time = 2
k = 5
time_per_k_turns = 1


game1 = GameRunner(setup_time, time_per_k_turns, k, 'n', "better_player", "simple_player")
print("Random player starts:")
for i in range(3):
    game1.run()

game2 = GameRunner(setup_time, time_per_k_turns, k, 'n', "simple_player", "better_player")
print("Simple player starts:")
for i in range(3):
    game2.run()