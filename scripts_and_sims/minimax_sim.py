from run_game import GameRunner
from players.better_player import setStaticConf
from players import simple_player, random_player

setup_time = 2
k = 5
time_per_k_turns = 1
verb = 'n'
res = ""
num_games = 10

def playAgainstEachOther(str1, str2):
    print(str1, " VS ", str2, "\n")
    game1 = GameRunner(setup_time, time_per_k_turns, k, verb, str1, str2)
    game2 = GameRunner(setup_time, time_per_k_turns, k, verb, str2, str1)

    player1_wins_as_O = 0
    player2_wins_as_O = 0
    player1_wins_as_X = 0
    player2_wins_as_X = 0

    print(str1, " starts:")
    for i in range(num_games):
        res = game1.run()
        if res[0] == 'O':
            player2_wins_as_O += 1
        elif res[0] == 'X':
            player1_wins_as_X += 1

    print(str1, " X wins = ", player1_wins_as_X)
    print(str2, " O wins = ", player2_wins_as_O)

    print(str2, " starts:")
    for i in range(num_games):
        res = game2.run()
        if res[0] == 'O':
            player1_wins_as_O += 1
        elif res[0] == 'X':
            player2_wins_as_X += 1

    print(str1, " O wins = ", player1_wins_as_O)
    print(str2, " X wins = ", player2_wins_as_X)

    print("\n")
    print(str1, " tot wins = ", player1_wins_as_O+player1_wins_as_X)
    print(str2, " tot wins = ", player2_wins_as_X+player2_wins_as_O)
    print("\n")


#playAgainstEachOther("needo_player", "better_player")
"""
for i in range(8):
    setStaticConf(i)
    print("\n\n Trying CONF #", i, "\n\n")
    playAgainstEachOther("min_max_player", "simple_player")
    playAgainstEachOther("min_max_player", "needo_player")
    playAgainstEachOther("min_max_player", "better_player")

exit(0)
"""
setStaticConf(0)
playAgainstEachOther("min_max_player", "simple_player")
playAgainstEachOther("min_max_player", "needo_player")
playAgainstEachOther("min_max_player", "better_player")
