import game

"""This is a test game, meaning a test of running a single game between two
random agents. Later, we can run experiments in this way."""

print('Creating the game...')

#create a game with an MCTS and RHEA player (not yet implemented)
test_game = game.Game('Random', 'Random')

#print off map
#test_game.print_map()

print('Getting starting positions...')

#choose random starting positions for the 2 players
test_game.random_starting_positions()

print('Getting moves for both players...')

#has the players each choose the set of moves they want to make
test_game.get_moves()

player1_owned = test_game.player1.get_owned_countries()
player2_owned = test_game.player2.get_owned_countries()

print('player 1 owns: ' + str(player1_owned))
print('player 2 owns: ' + str(player2_owned))

print('Performing moves for both players...')

#perform the array of moves in alternating order
test_game.perform_moves_in_order()

print('Moves performed...')

player1_owned = test_game.player1.get_owned_countries()
player2_owned = test_game.player2.get_owned_countries()

print('player 1 owns: ' + str(player1_owned))
print('player 2 owns: ' + str(player2_owned))

#print off map
test_game.print_map()



#player1 = test_game.player1.get_owned_countries()
#print('Player 1 countries owned before making moves...')
#print(player1)



#player1 = test_game.player1.get_owned_countries()
#print('Player 1 countries owned after making moves...')
#print(player1)





