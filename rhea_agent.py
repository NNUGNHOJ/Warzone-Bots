from copy import deepcopy
import random
import itertools


class RHEA_agent:
    # set random seed
    random.seed(10)

    def __init__(self, colour):
        self.colour = colour
        self.indivdualSize = 10
        self.populationSize = 10
        self.numGenerations = 10
        self.numParents = 2
        self.mutationLen = 1
        self.elite = 3
        self.tournament_size = 5
        self.maxMoves = 3

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

    def performAction(self, action, owned_countries):
        # assuming copies of the objects are given when necessary
        from_country = action[0]
        to_country = action[1]
        number = action[2]

        # add to new country
        if (to_country in owned_countries):
            owned_countries[str(to_country)] += number
        else:
            owned_countries[str(to_country)] = number

        # subtract from old country if it's still there
        owned_countries[str(from_country)] -= number

    def evaluateIndividual(self, individual, map, owned_countries):
        # make copy of the map and owned countries
        map_copy = deepcopy(map)
        owned_countries_copy = deepcopy(owned_countries)

        for i in range(len(individual) - 1):
            action = individual[i]
            possible_moves = self.get_possible_moves(owned_countries_copy, map_copy)
            if action in possible_moves:
                self.performAction(action, owned_countries_copy)
            else:
                # random action
                action = possible_moves[random.randint(0, len(possible_moves) - 1)]
                self.performAction(action, owned_countries_copy)
            # check if gameover
            if len(owned_countries_copy) == 0:
                return -100

        # otherwise return score
        # number of countries
        fitness = len(owned_countries_copy)

        return fitness

    def evaluateAction(self, action, map, owned_countries):
        # make copy of the map and owned countries
        map_copy = deepcopy(map)
        owned_countries_copy = deepcopy(owned_countries)

        # do action
        self.performAction(action, owned_countries_copy)

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
                self.performAction(action, owned_countries_copy)

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
                self.performAction(best_action, owned_countries_copy)

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
        print(str(self.colour) + ' owns these countries: ' + str(owned_countries))
        # begin here
        population = []
        population_scores = []
        all_moves = []
        new_score = -1
        old_score = -2
        moves = 0
        reinf_cards_played = 0
        # initialize population
        for i in range(self.populationSize):
            population.append(self.OneSLA(map, owned_countries))
            population_scores.append(self.evaluateIndividual(population[i], map, owned_countries))

        while new_score > old_score and moves <= self.maxMoves:
            moves += 1
            old_score = new_score
            # while time not elapsed:
            for j in range(10):
                population, population_scores = self.runIteration(population, population_scores, map, owned_countries)
                # sort on decreasing value
                population = [x for _, x in sorted(zip(population_scores, population), reverse=True)]
                population_scores.sort(reverse=True)

            # return best action, reinf_cards_played, owned_countries
            best_inidvidual = population[0]
            new_score = population_scores[0]
            if best_inidvidual[0] not in self.get_possible_moves(owned_countries, map):
                continue

            #print('BEST ACTION', best_inidvidual[0])
            all_moves.append(best_inidvidual[0])
            self.performAction(best_inidvidual[0], owned_countries)
        print(str(self.colour) + ' does these moves: ' + str(all_moves))
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

        #get all permutations
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

    def allocate_armies(self, additional_armies, owned_countries):
        possible_allocations = self.get_possible_allocations(additional_armies, owned_countries)

        best_score = 0

       # for allocation in possible_allocations:
            #I can't call choosemoves here and return things because we don't have those parameters

        #so we have to do random:
        return random.choice(possible_allocations)
