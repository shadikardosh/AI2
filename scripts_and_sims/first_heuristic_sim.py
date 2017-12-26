from run_game import GameRunner
from players import simple_player, random_player

setup_time = 2
k = 5
time_per_k_turns = 1
res = ""

full_game1 = GameRunner(setup_time, time_per_k_turns, k, 'y', "better_player", "simple_player")
full_game2 = GameRunner(setup_time, time_per_k_turns, k, 'y', "simple_player", "better_player")
#full_game1.run()
#full_game2.run()
print("BETTER VS SIMPLE")
game1 = GameRunner(setup_time, time_per_k_turns, k, 'n', "better_player", "simple_player")
print("Better player starts:")
for i in range(5):
    res = game1.run()

game2 = GameRunner(setup_time, time_per_k_turns, k, 'n', "simple_player", "better_player")
print("Simple player starts:")
for i in range(5):
    game2.run()

print("B1 VS SIMPLE")
game1 = GameRunner(setup_time, time_per_k_turns, k, 'n', "b1_player", "simple_player")
print("b1_player  starts:")
for i in range(5):
    res = game1.run()

game2 = GameRunner(setup_time, time_per_k_turns, k, 'n', "simple_player", "b1_player")
print("Simple player starts:")
for i in range(5):
    game2.run()

print("BETTER VS B1")
game1 = GameRunner(setup_time, time_per_k_turns, k, 'n', "better_player", "b1_player")
print("Better player starts:")
for i in range(5):
    res = game1.run()

game2 = GameRunner(setup_time, time_per_k_turns, k, 'n', "b1_player", "better_player")
print("b1_player starts:")
for i in range(5):
    game2.run()