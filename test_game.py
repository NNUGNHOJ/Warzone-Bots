import game
import matplotlib.pyplot as plt

print('Creating the game...')

#create a game with an MCTS and RHEA player (not yet implemented)
test_game = game.Game('Random', 'Random')

print('Getting starting positions...')

#choose random starting positions for the 2 players
test_game.random_starting_positions()

player1_owned = test_game.player1.get_owned_countries()
player2_owned = test_game.player2.get_owned_countries()

print('player 1 owns: ' + str(player1_owned))
print('player 2 owns: ' + str(player2_owned))

number_of_rounds = 150
map_states = []
results = []

for i in range(number_of_rounds):
    print('Getting moves for both players...')
    #has the players each choose the set of moves they want to make
    test_game.get_moves()
    print('Performing moves for both players...')
    #perform the array of moves in alternating order
    test_game.perform_moves_in_order()
    #append the map at the end of the turn to an array
    map_states.append(test_game.map_graph)
    results.append(test_game.map_graph.get_turn_statistics())

#print off map
test_game.print_map()

"""Collect statistics and plot"""
player1_countries = []
player2_countries = []
countries = []
index = []

for result in results:
    print(result)
    player1_countries.append(len(result[0]))
    player2_countries.append(len(result[1]))
    countries.append(len(result[2]))

count = 1
for i in range(len(player2_countries)):
    index.append(count)
    count += 1

plt.plot(index, player1_countries, label="Player 1")
plt.plot(index, player2_countries, label="Player 2")
plt.xlabel('Turn')
plt.ylabel('Countries owned')
plt.title('Number of countries owned for Random vs Random')
plt.legend()
plt.show()










