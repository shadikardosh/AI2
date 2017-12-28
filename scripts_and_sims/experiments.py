from run_game import GameRunner
import csv
# game parameters
setup_time = 2
k = 5
time_per_k_turns = 2
verb = 'n'
num_games = 5

stats = open('sex.csv', 'w')

def playAgainstEachOther(str1, str2):
    print("##################################")
    print(str1, " VS ", str2, "\n")
    game1 = GameRunner(setup_time, time_per_k_turns, k, verb, str1, str2)
    game2 = GameRunner(setup_time, time_per_k_turns, k, verb, str2, str1)

    player1_wins_as_O = 0
    player2_wins_as_O = 0
    player1_wins_as_X = 0
    player2_wins_as_X = 0
    ties = 0

    print(str1, " starts:")
    for i in range(num_games):
        player1_score = 0
        player2_score = 0
        res = game1.run()
        if res[0] == 'O':
            player2_score = 1
        elif res[0] == 'X':
            player1_score = 1
        else:
            ties += 1
            player1_score, player2_score = 0.5, 0.5

        player1_wins_as_X, player2_wins_as_O = player1_wins_as_X+player1_score, \
                                               player2_wins_as_O+player2_score
        stats_writer = csv.writer(stats, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        stats_writer.writerow([str1, str2, time_per_k_turns, player1_score, player2_score])

    #print(str1, " X wins = ", player1_wins_as_X)
    #print(str2, " O wins = ", player2_wins_as_O)

    print(str2, " starts:")
    for i in range(num_games):
        player1_score = 0
        player2_score = 0
        res = game2.run()
        if res[0] == 'O':
            player1_score = 1
        elif res[0] == 'X':
            player2_score = 1
        else:
            ties += 1
            player1_score, player2_score = 0.5, 0.5

        player1_wins_as_O, player2_wins_as_X = player1_wins_as_O+player1_score, \
                                               player2_wins_as_X+player2_score
        stats_writer = csv.writer(stats, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        stats_writer.writerow([str2, str1, time_per_k_turns, player2_score, player1_score])

    player1_total_wins = player1_wins_as_O+player1_wins_as_X
    player2_total_wins = player2_wins_as_X+player2_wins_as_O

    #print(str1, " O wins = ", player1_wins_as_O)
    #print(str2, " X wins = ", player2_wins_as_X)

    print("")
    print(str1, " tot wins = ", player1_total_wins)
    print(str2, " tot wins = ", player2_total_wins)
    print("")
    #print("##################################")

    return player1_total_wins, player2_total_wins


players_names = ["simple_player", "better_player", "min_max_player", "alpha_beta_player"]
spaces = ["       ", "       ", "      ", "   "]
players_scores_according_to_t = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
T = [2, 10, 50]

for t in range(len(T)):
    print("##################################")
    print("##################################")
    print("## t IS EQUAL TO ", T[t])
    time_per_k_turns = T[t]
    for i in range(4):
        for j in range(i):
            res = playAgainstEachOther(players_names[i], players_names[j])
            players_scores_according_to_t[t][i] += res[0] + 0.5 * (2*num_games - (res[0] + res[1]))
            players_scores_according_to_t[t][j] += res[1] + 0.5 * (2*num_games - (res[0] + res[1]))
    print("##################################")

# print each player's scores:
print("\n\n")
print("##################################")
print("# PRINTING SCORES ")
print("##################################")
print("\n")

for t in range(3):
    print("## When t IS EQUAL TO ", T[t])
    for i in range(4):
        print("### ",players_names[i], "'s SCORE IS:", spaces[i], players_scores_according_to_t[t][i])

stats.close()
