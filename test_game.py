import game

#create a game with an MCTS and RHEA player (not yet implemented)
test_game = game.Game('MCTS', 'RHEA')

#choose random styarting positions for the 2 players
test_game.random_starting_positions()

#print off map
test_game.print_map()