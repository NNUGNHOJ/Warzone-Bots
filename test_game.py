import game
import matplotlib.pyplot as plt

def print_stats(results):
    """Collect statistics and plot"""
    player1_countries = []
    player2_countries = []
    countries = []
    index = []

    for result in results:
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


def game_based_on_number_of_rounds(player1, player2, number_of_rounds, print_map, print_graph):
    #create a game two Random players
    test_game = game.Game(str(player1), str(player2))

    #choose random starting positions for the 2 players
    test_game.random_starting_positions()

    map_states = []
    results = []

    for i in range(number_of_rounds):
        #has the players each choose the set of moves they want to make
        test_game.get_moves()
        #perform the array of moves in alternating order
        test_game.perform_moves_in_order()
        #append the map at the end of the turn to an array
        map_states.append(test_game.map_graph)
        results.append(test_game.map_graph.get_turn_statistics())

    if print_map:
        # print off map
        test_game.print_map()

    if print_graph:
        print_stats(results)


def game_based_on_win_criteria(player1, player2, print_map, print_graph):
    # create a game two Random players
    test_game = game.Game(str(player1), str(player2))

    # choose random starting positions for the 2 players
    test_game.random_starting_positions()

    map_states = []
    results = []
    game_over = False

    while not game_over:
        #check if the game is over
        test_game.check_game_over()
        # has the players each choose the set of moves they want to make
        test_game.get_moves()
        # perform the array of moves in alternating order
        test_game.perform_moves_in_order()
        # append the map at the end of the turn to an array
        map_states.append(test_game.map_graph)
        results.append(test_game.map_graph.get_turn_statistics())

    if print_map:
        # print off map
        test_game.print_map()

    if print_graph:
        print_stats(results)


#play a game which ends only when one of the 2 players doesn't own any countries anymore
# NOTE: this doesnt always work for the random agents because sometimes they're just too
# dumb to actually win a game

#game_based_on_win_criteria('Random', 'Random', True, False)

#play game based on a maximum number of rounds
game_based_on_number_of_rounds('Random', 'Random', 30, True, False)












