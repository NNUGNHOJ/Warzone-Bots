import game

"""This is a test game, meaning a test of running a single game between two
random agents. Later, we can run experiments in this way."""

#create a game with an MCTS and RHEA player (not yet implemented)
test_game = game.Game('Random', 'Random')

#choose random starting positions for the 2 players
test_game.random_starting_positions()

#print off map
test_game.print_map()

#has the players each choose the set of moves they want to make
test_game.get_moves()

#perform the array of moves in alternating order
test_game.perform_moves_in_order()

#print off map
test_game.print_map()