import game

#create a game with an MCTS and RHEA player (not yet implemented)
test_game = game.Game('Random', 'Random')

#choose random styarting positions for the 2 players
test_game.random_starting_positions()

#print off map
test_game.print_map()

#has the players each choose the set of moves they want to make
test_game.get_moves()

