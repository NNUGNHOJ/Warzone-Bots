from copy import deepcopy
import random
import itertools
import map
import time


class RHEA_agent:
    # set random seed
    # random.seed(10)

    def __init__(self, colour):
        self.colour = colour
        self.indivdualSize = 10
        self.populationSize = 1
        self.numGenerations = 10
        self.numParents = 2
        self.mutationLen = 1
        self.elite = 1 #don't forget to change to three
        self.tournament_size = 5
        self.maxMoves = 3
        self.actions = None

    def get_possible_moves(self, owned_countries, map):
        """Get all the possible moves the agent could make"""
        current_owned_countries = owned_countries
        possible_moves = []

        for country in list(current_owned_countries.keys()):
            current_neighbours = [n for n in map.map_graph.neighbors(country)]
            current_armies_count = current_owned_countries[str(country)]
            for neighbour in current_neighbours:
                for i in range(current_armies_count):
                    possible_moves.append((str(country), str(neighbour), i + 1))

        return possible_moves

    def adjust_map(self, player1_owned_countries, player2_owned_countries, state, map):
        """Changes the map to reflect the owned countries and army counts as per the players"""
        # for country in player1_owned_countries.keys():
        for country, value in player1_owned_countries.items():
            map.change_colour(str(country), 'b')
            map.set_army_count(str(country), player1_owned_countries[str(country)])

        # for country in player2_owned_countries.keys():
        for country, value in player2_owned_countries.items():
            map.change_colour(str(country), 'r')
            map.set_army_count(str(country), player2_owned_countries[str(country)])
        return map

    def performAction(self, action, owned_countries, map, state):
        """Takes a single move and performs it on the map graph, a move consists
                of (origin_country, destination_country, armies_to_move)"""
        if self.colour == 'b':
            attacking_player_colour = 'b'
            """If destination_country isn't owned by either player"""
            if map.get_colours_dict()[action[1]] == 'k':
                defending_player_colour = 'k'
            elif map.get_colours_dict()[action[1]] == 'b':
                defending_player_colour = None
            else:
                defending_player_colour = 'r'
        else:
            attacking_player_colour = 'r'
            """destination_country isn't owned by either player"""
            if map.get_colours_dict()[action[1]] == 'k':
                defending_player_colour = 'k'
            elif map.get_colours_dict()[action[1]] == 'r':
                defending_player_colour = None
            else:
                defending_player_colour = 'b'
        """Check that the player still owns the origin_country, if it does not, 
        then return without making the move."""
        if map.get_colours_dict()[action[0]] != str(self.colour):
            return

        """Check if the origin country still has all the armies the move wants to
        utilise"""

        """If the origin_country does not have as many armies as the move
        requires, then just use however many armies there are left."""
        if map.get_armies_dict()[action[1]] >= action[2]:
            attacking_player_armies = action[2]
        else:
            attacking_player_armies = map.get_armies_dict()[action[0]]

        """If the same player owns both countries, just transfer the armies"""
        if map.get_colours_dict()[action[0]] == map.get_colours_dict()[action[1]]:
            origin_army_count = map.get_armies_dict()[action[0]]
            destination_army_count = map.get_armies_dict()[action[0]]

            map.set_army_count(action[0], (origin_army_count - attacking_player_armies))
            map.set_army_count(action[1], (destination_army_count + attacking_player_armies))
            #             attacking_player.add_owned_country(str(move[0]), (origin_army_count - attacking_player_armies))
            #             attacking_player.add_owned_country(str(move[1]), (destination_army_count + attacking_player_armies))
            state.update({action[1]: destination_army_count + attacking_player_armies})
            state[action[0]] = origin_army_count - attacking_player_armies

            return

        """Check if defending country is a player, and not a black node, if it
        is a player, they will have an associate owned_countries dict which has
        to be adjusted"""
        if defending_player_colour == 'r':
            defending_player_owned_countries = {}
            armies = map.get_armies_dict()
            countries_colour = map.get_colours_dict()
            for i in range(len(countries_colour)):
                key = list(countries_colour.keys())[i]
                if countries_colour[key] == 'r':
                    defending_player_owned_countries.update({key: armies[key]})

            defending_player_armies = defending_player_owned_countries[action[1]]
        elif defending_player_colour == 'b':
            defending_player_owned_countries = {}
            armies = map.get_armies_dict()
            countries_colour = map.get_colours_dict()
            for i in range(len(countries_colour)):
                key = list(countries_colour.keys())[i]
                if countries_colour[key] == 'b':
                    defending_player_owned_countries.update({key: armies[key]})
            defending_player_armies = defending_player_owned_countries[action[1]]
        else:
            """If the country isn't owned by anyone, it has 2 armies"""
            defending_player_armies = map.get_armies_dict()[action[1]]

        """For every army attacking, get outcome of a single attack"""
        for i in range(attacking_player_armies):
            """If there are still defending armies in destination_country"""
            if map.get_armies_dict()[action[1]] > 0:

                defender_chance = random.randint(0, 100)  # <= 70 means defender wins
                attacker_chance = random.randint(0, 100)  # <= 60 means attacker wins

                """If both players successfully roll, nothing happens"""

                """If defender successfully rolls but attacker doesnt, kill one
                attacking army, defending army stays the same"""
                if defender_chance <= 70 and attacker_chance > 60:
                    new_value = state[action[0]] - 1
                    attacking_player_armies -= 1  # may be able to remove this line entirely
                    state[action[0]] = new_value
                    #                     attacking_player.add_owned_country(str(move[0]), new_value)
                    map.set_army_count(action[0], new_value)

                """If attacking army successfully rolls but defender doesnt, kill one
                defending army, attacking army stays the same"""
                if defender_chance > 70 and attacker_chance <= 60:
                    if defending_player_colour == 'r' or defending_player_colour == 'b':

                        new_value = map.get_armies_dict()[action[1]] - 1

                        defending_player_owned_countries.update({action[1]: new_value})

                        map.set_army_count(action[1], new_value)


                    else:
                        """No one owns the defending country, so just remove one army in the map object"""
                        value = map.get_armies_dict()[action[1]] - 1
                        map.set_army_count(action[1], value)

            """Else there are no defending armies anymore, flip country to attacking player and
            add the remaining armies to it"""
            if map.get_armies_dict()[action[1]] == 0:
                state.update({action[1]: attacking_player_armies})

                map.set_army_count(action[1], attacking_player_armies)
                map.change_colour(action[1], self.colour)

                """If destination_country is owned by the opposing player"""
                if defending_player_colour == 'r' or defending_player_colour == 'b':
                    defending_player_owned_countries.pop(action[1])

            if defending_player_armies < 0:
                print('Army count has gone below 0...')

        """Adjust the game map to reflect the new game state after the move"""
        if defending_player_colour == 'r':
            map = self.adjust_map(state, defending_player_owned_countries, state, map)
        elif defending_player_colour == 'b':
            map = self.adjust_map(state, defending_player_owned_countries, state, map)
        else:
            map = self.adjust_map(state, {}, state, map)

        new_owned_countries = {}
        for key, value in map.colours.items():
            if value == self.colour:
                army_in_country = map.armies[str(key)]
                new_owned_countries[str(key)] = army_in_country

        return

    def score_additional_armies(self, owned_countries):
        total_armies = 5
        map_graph = map.Map()
        region_dict = map_graph.regions_dict
        countries_owned_by_player = owned_countries

        """Check if player owns any entire regions, allocate extra armies if they do"""
        for region in region_dict.keys():
            total_countries_in_region = len(region)
            player_countries_count_in_region = 0
            for country in region:
                if str(country) in countries_owned_by_player.keys():
                    player_countries_count_in_region += 1
            """If the player owns all the countries in a region, they get a bonus"""
            if player_countries_count_in_region == total_countries_in_region:
                regions_bonus_dict = map_graph.get_bonus_dict()
                bonus = regions_bonus_dict[str(region)]
                total_armies += bonus

        return total_armies

    def evaluateIndividual(self, individual, map, owned_countries):
        # make copy of the map and owned countries
        map_copy = deepcopy(map)
        owned_countries_copy = deepcopy(owned_countries)

        for i in range(len(individual) - 1):
            action = individual[i]
            possible_moves = self.get_possible_moves(owned_countries_copy, map_copy)
            if action in possible_moves:
                self.performAction(action, owned_countries_copy, map_copy, owned_countries_copy)
            else:
                # random action
                if len(possible_moves) >= 1:
                    action = possible_moves[random.randint(0, len(possible_moves) - 1)]
                else:
                    return -100
                self.performAction(action, owned_countries_copy, map_copy, owned_countries_copy)
            # check if gameover
            if len(owned_countries_copy) == 0:
                return -100

        # difference in boarder unints
        """
        looking to establish a measure which shows strength of force against direct threats
        TODO:
            - check how many countries are boardering enemy units
            - add unit totals against foreign units (country by country)
            - should we return a % of boardering countries that have a dominating force?
        """
        num_dominating_countries = 0
        dominating_score = 0
        boarder_countries = []
        enemy_owned_countries = {}
        if (self.colour == 'r'):
            enemy_colour = 'b'
        else:
            enemy_colour = 'r'
        # get dict with all enemies
        for key, value in map.colours.items():
            if value != self.colour:
                army_in_country = map.armies[str(key)]
                enemy_owned_countries[str(key)] = army_in_country

        for country in list(owned_countries_copy.keys()):
            boarder_countries = [n for n in map.map_graph.neighbors(country)]
            country_armies = map.get_armies_dict()[str(country)]
            for boarder_country in boarder_countries:
                if map.get_colours_dict()[str(boarder_country)] == enemy_colour:
                    # enemy country, check if we have more armies than can be allocated bny the opponent
                    num_allocations_enemy = self.score_additional_armies(enemy_owned_countries)

                    #get current number of armies for both
                    enemy_country_armies = map.get_armies_dict()[str(boarder_country)]

                    if (country_armies > (enemy_country_armies + num_allocations_enemy)):
                        #or percentage
                        num_dominating_countries += 1

        percentage_dominating = num_dominating_countries / len(owned_countries_copy.keys())
        # otherwise return score
        # number of countries
        fitness = len(owned_countries_copy)

        # score for additional armies
        add_score = self.score_additional_armies(owned_countries)

        return (10*fitness) + (5 * add_score) + (percentage_dominating*100)


    def evaluateAction(self, action, map, owned_countries):
        # make copy of the map and owned countries
        map_copy = deepcopy(map)
        owned_countries_copy = deepcopy(owned_countries)

        # do action
        self.performAction(action, owned_countries_copy, map_copy, owned_countries_copy)

        # evaluate
        fitness = len(owned_countries_copy)

        return fitness

    def OneSLA(self, map, owned_countries):
        # to initialize the population we use 1SLA
        individual = []
        # make copy of the map and owned countries
        map_copy = deepcopy(map)
        owned_countries_copy = deepcopy(owned_countries)

        for i in range(self.indivdualSize):
            if i == 0:
                # get random action
                possible_actions = self.get_possible_moves(owned_countries_copy, map_copy)
                n = random.randint(0, len(possible_actions) - 1)
                action = possible_actions[n]
                individual.append(action)
                # do action
                self.performAction(action, owned_countries_copy, map_copy, owned_countries_copy)

            else:
                best_score = 0

                # loop over all possible actions to find best action
                possible_actions = self.get_possible_moves(owned_countries_copy, map_copy)
                for action in possible_actions:
                    score = self.evaluateAction(action, map_copy, owned_countries_copy)

                    if score > best_score:
                        best_score = score
                        best_action = action
                individual.append(best_action)

                # do action
                self.performAction(best_action, owned_countries_copy, map_copy, owned_countries_copy)

        return individual

    def crossover(self, parent1, parent2):
        # single point crossover
        # choose a point
        n = random.randint(0, self.indivdualSize - 1)
        child = []
        for i in range(len(parent1)):
            if i < n:
                child.append(parent1[i])
            else:
                child.append(parent2[i])
        return child

    def selection(self, population, population_scores):
        # #Tournament selection:
        # The algorithm choose randomly five  individuals from the population and returns the fittest one

        # randomly choose 5 numbers and return the best parent
        bestScore = -1000
        for i in range(self.tournament_size):
            n = random.randint(0, self.populationSize - 1)
            score = population_scores[n]
            if score > bestScore:
                bestIndividual = n

        return population[bestIndividual]

    def mutation(self, child, map, owned_countries):
        # Mutate one place
        n = random.randint(0, len(child) - 1)

        possible_moves = self.get_possible_moves(owned_countries, map)
        i = random.randint(0, len(possible_moves) - 1)
        new_move = possible_moves[i]
        child[n] = new_move
        return child

    def runIteration(self, population, population_scores, map, owned_countries):
        # Run evolutionary process for one generation
        new_population = []
        new_population_scores = []
        # elite best offspring are crossed over immediatly
        for i in range(self.elite):
            new_population.append(population[i])
            new_population_scores.append(population_scores[i])

        temp_population = []
        temp_population_scores = []
        # generate P offspring
        for j in range(self.populationSize):
            # select two parent by tournament selection
            parent1 = self.selection(population, population_scores)
            parent2 = self.selection(population, population_scores)

            # uniform crossover to create a child
            child = self.crossover(parent1, parent2)
            # mutate the child
            mutated_child = self.mutation(child, map, owned_countries)

            # add to temp population
            temp_population.append(list(mutated_child))

        # generate scores for temp pop
        for k in range(self.populationSize):
            fitness = self.evaluateIndividual(temp_population[k], map, owned_countries)
            temp_population_scores.append(fitness)

        # sort them
        temp_population = [x for _, x in sorted(zip(temp_population_scores, temp_population), reverse=True)]
        temp_population_scores.sort(reverse=True)

        # the best num of individuals - elite are chosen to the next gen
        m = 0
        for l in range(self.elite, self.populationSize):
            new_population.append(temp_population[m])
            new_population_scores.append(temp_population_scores[m])
            m += 1

        return new_population, new_population_scores

    def choose_moves(self, map, colour, owned_countries, reinf_card_count):
        print("rhea agent is: ", colour)
       # print("CHOOSE MOVES COLOUR DIC BEFORE", map.get_colours_dict())
        map2 = deepcopy(map)
        self.map = deepcopy(map2)
        owned_countries2 = deepcopy(owned_countries)
        t0 = time.clock()
        print(str(self.colour) + ' owns these countries: ' + str(owned_countries))
        #begin here
        population = []
        population_scores = []
        all_moves = []
        new_score = -1
        old_score = -2
        moves = 0
        reinf_cards_played = 0
        time_elapsed = 0
        time_per_move = 0
        max_time = 20
        self.actions = self.get_possible_moves(owned_countries2, self.map)
        state = owned_countries2

        # initialize population
        for i in range(self.populationSize):
            population.append(self.OneSLA(map, owned_countries2))
            population_scores.append(self.evaluateIndividual(population[i], map,owned_countries2))

        while (new_score > old_score) and (moves <= self.maxMoves):
            self.actions = self.get_possible_moves(owned_countries2, map)
            moves += 1
            old_score = new_score
            # while time not elapsed:
            for j in range(10):
                population, population_scores = self.runIteration(population, population_scores, map, owned_countries2)
                # sort on decreasing value
                population = [x for _, x in sorted(zip(population_scores, population), reverse=True)]
                population_scores.sort(reverse=True)

            # return best action, reinf_cards_played, owned_countries
            best_inidvidual = population[0]
            new_score = population_scores[0]
            if best_inidvidual[0] not in self.get_possible_moves(owned_countries2, map):
                continue

            # print('BEST ACTION', best_inidvidual[0])
            all_moves.append(best_inidvidual[0])
            self.performAction(best_inidvidual[0], owned_countries2, map, owned_countries2)

            # updated time
            time_elapsed = time.clock() - t0
            time_per_move = time_elapsed / moves

        print(str(self.colour) + ' does these moves: ' + str(all_moves))
        print(str(self.colour) + ' has these countries: ' + str(owned_countries))
        #print("CHOOSE MOVES COLOUR DIC AFTER", map.get_colours_dict())
        return all_moves, reinf_cards_played, owned_countries

    def consider_reinf_card(self, reinf_card_count):
        # what to do here?
        # return number of reinforcements card
        # I can't call choosemoves here and return things because we don't have those parameters

        return random.randint(0, reinf_card_count)

    # Recursive function to print all combinations of numbers from `i` to `n`
    # having sum `n`. The `index` denotes the next free slot in the output list `out`
    def getCombinations(self, i, n, out, index, combis, num_countries):

        # if the sum becomes `n`, print the combination
        if n == 0 and (len(out[:index])) == num_countries:
            combis.append(out[:index])

        # start from the previous element in the combination till `n`
        for j in range(i, n + 1):
            # place current element at the current index
            if index > num_countries - 1:
                continue
            out[index] = j

            # recur with a reduced sum
            self.getCombinations(j, n - j, out, index + 1, combis, num_countries)

    def get_possible_allocations(self, additional_armies, owned_countries):
        all_possible_owned_countries = []
        combis_all = []

        # get all possible combinations of the additional_armies
        combis = []
        num_countries = len(owned_countries)
        out = [None] * num_countries
        self.getCombinations(0, additional_armies, out, 0, combis, num_countries)

        # get all permutations
        for comb in combis:
            permu = list(itertools.permutations(comb))
            for i in permu:
                combis_all.append(i)

        for combi in combis_all:
            j = 0
            copy_countries = deepcopy(owned_countries)
            for key in copy_countries:
                copy_countries[key] += combi[j]
                j += 1
            all_possible_owned_countries.append(copy_countries)

        return all_possible_owned_countries

    def allocate_armies(self, additional_armies, owned_countries, map):
        """Takes in a number of armies to be allocated, works out which countries most
                 need additional armies. Then allocates armies based on a probability distribution,
                 where countries that need armies are more likely to get given them. Then returns
                 the owned_countries dict"""
        print("ALLOCATING ARMIES COLOUR DIC BEFORE", map.get_colours_dict())
        current_owned_countries = deepcopy(owned_countries)
        neighbouring_countries = []
        placement_probability_dict = owned_countries

        """set initial probabilities to 0"""
        for key, value in placement_probability_dict.items():
            placement_probability_dict[str(key)] = 0

        """For each country, work out how many armies to give it"""
        for country in list(current_owned_countries.keys()):
            neighbouring_countries.append([n for n in map.map_graph.neighbors(country)])

            """check if any neighbouring countries have opponent armies"""
            for neighbouring_country in neighbouring_countries[0]:
                """If neighbour colour not the same as player colour"""
                if map.get_colours_dict()[str(neighbouring_country)] != str(self.colour):
                    """If neighbouring country isn't owned by anyone, just add 1"""
                    if map.get_colours_dict()[str(neighbouring_country)] == 'b':
                        placement_probability_dict[str(country)] += 1
                    else:
                        """If country already has an overwhelming number of armies, dont bother adding more, save 
                        them for some other country"""
                        if (map.get_armies_dict()[str(neighbouring_country)] * 1.5) >= map.get_armies_dict()[
                            str(country)]:
                            placement_probability_dict[str(country)] += 1
                        else:
                            """Add probability based on how many armies are in that neighbouring country"""
                            placement_probability_dict[str(country)] += map.get_armies_dict()[str(neighbouring_country)]

        """Allocate the armies based on the collected probability distribution"""

        """Turn values into probabilities of allocating"""
        total = 0
        list_of_candidates = [*placement_probability_dict]
        probability_distribution = []

        for key, item in placement_probability_dict.items():
            total += item

        for key, item in placement_probability_dict.items():
            placement_probability_dict[str(key)] = item / total
            probability_distribution.append(item / total)

        """Choose countries 'randomly' but weighted based on probability distribution"""
        chosen_countries = random.choices(population=list_of_candidates,
                                          weights=probability_distribution,
                                          k=additional_armies)


        """Allocate the chosen countries"""
        for country in chosen_countries:
            current_owned_countries[str(country)] += 1

        print("AFTER ALLOCATING RHEA now has these countries:", current_owned_countries)
        print("ALLOCATING ARMIES COLOUR DIC BEFORE", map.get_colours_dict())
        return current_owned_countries
