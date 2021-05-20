import game
import matplotlib.pyplot as plt

def print_stats(results,NUM_GAMES):
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

    # Number of countries owned
    player_1_countries_owned = player1_countries[len(player1_countries) - 1]
    player_2_countries_owned = player2_countries[len(player2_countries) - 1]

    plt.plot(index, player1_countries, label="Player 1")
    plt.plot(index, player2_countries, label="Player 2")
    plt.xlabel('Turn')
    plt.ylabel('Countries owned')
    plt.title('Number of countries owned for Heuristic vs MCTS')
    plt.legend()
    plt.show()
    plt.savefig('MCTS30'+str(NUM_GAMES))

    return player_1_countries_owned, player_2_countries_owned


def game_based_on_number_of_rounds(player1, player2, number_of_rounds, print_map, print_graph,NUM_GAMES,txt_file):
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
        
       
       
         #number of countries owned
        player_1_countries_owned = []
        player_2_countries_owned=[]
        
        for country in list(test_game.map_graph.get_colours_dict().keys()):
            if test_game.map_graph.get_colours_dict()[country]=='b':
                player_1_countries_owned.append((country,test_game.map_graph.get_armies_dict()[country]))
            elif test_game.map_graph.get_colours_dict()[country]=='r':
                player_2_countries_owned.append((country,test_game.map_graph.get_armies_dict()[country]))
        txt_file.write("Number of countries owned by player 1 in round: "+str(i) + str(player_1_countries_owned) + "\n")
        txt_file.write("Number of countries owned by player 2 in round: "+str(i) + str(player_2_countries_owned) + "\n")
       
        
        
        
    if print_map:
        # print off map
        test_game.print_map()

    if print_graph:
        results = print_stats(results,NUM_GAMES)

    return results, test_game, txt_file



def MCTS_testing():
    #For now because of optimization we might need to limit it to a number of turn so
    #i'm using the game based on number of rounds function
    NUM_GAMES = 10
    specifications = "MCTS_Heuristic_rollout=30" #adjust this
    filename = "Results_" + specifications + ".txt"
    f = open(filename, "w")
    for i in range(NUM_GAMES):
        f.write("Game: " + str(i) + "\n")
        f.write("Player 1: Heuristic, Player 2: MCTS" + "\n")
        results, test_game,f = game_based_on_number_of_rounds('Heuristic', 'MCTS', 25, True, True,NUM_GAMES,f)

        #number of countries owned
        player_1_countries_owned = results[0]
        player_2_countries_owned = results[1]
        f.write("Number of countries owned by player 1: " + str(player_1_countries_owned) + "\n")
        f.write("Number of countries owned by player 2: " + str(player_2_countries_owned) + "\n")

        #% land owned
        countries = test_game.map_graph.get_colours_dict()
        total_countries = len(countries.keys())
        percentage_p1 = player_1_countries_owned / total_countries
        percentage_p2 = player_2_countries_owned / total_countries

        f.write("% land owned by player 1: " + str(percentage_p1 * 100) + "\n")
        f.write("% land owned by player 2: " + str(percentage_p2 * 100) + "\n")

        #size of army versus opposing army
        armies_p1 = 0
        armies_p2 = 0
        armies = test_game.map_graph.get_armies_dict()
        print(countries)
        print(armies)
        for country in countries.keys():
            if countries[str(country)] == 'r':
                armies_p1 += armies[str(country)]
            elif countries[str(country)] == 'b':
                armies_p2 += armies[str(country)]

        f.write("Number of armies owned by player 1: " + str(armies_p1) + "\n")
        f.write("Number of armies owned by player 2: " + str(armies_p2) + "\n")

    f.close()
    return




MCTS_testing()








