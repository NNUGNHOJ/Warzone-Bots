import random

class Heuristic_agent:
    """Uses game heuristics only"""

    def __init__(self, colour):
        self.colour = colour
        self.enemy_countries = []
        self.empty_countries = []
        self.overwhelming_move = []
        self.defend_value_map = {
            'Alaska': 0, 'Northwest territory': 0, 'Greenland': 0, 'Alberta': 0,
            'Ontario': 0, 'Quebec': 0, 'Western United States': 0, 'Eastern United States': 0,
            'Mexico': 0, 'Venezuela': 0, 'Brazil': 0, 'Peru': 0, 'Argentina': 0,
            'North Africa': 0, 'Egypt': 0, 'East Africa': 0, 'Congo': 0, 'South Africa': 0,
            'Madagascar': 0, 'Iceland': 0, 'Scandinavia': 0, 'Great Britain': 0,
            'Northern Europe': 0, 'Western Europe': 0, 'Southern Europe': 0,
            'Ukraine': 0, 'Ural': 0, 'Siberia': 0, 'Yakutsk': 0, 'Kamchatka': 0,
            'Japan': 0, 'Mongolia': 0, 'Irkutsk': 0, 'China': 0, 'Siam': 0,
            'India': 0, 'Middle East': 0, 'Kazakhstan': 0, 'Indonesia': 0,
            'New Guinea': 0, 'Eastern Australia': 0, 'Western Australia': 0
        }
        self.attack_value_map = {
            'Alaska': 0, 'Northwest territory': 0, 'Greenland': 0, 'Alberta': 0,
            'Ontario': 0, 'Quebec': 0, 'Western United States': 0, 'Eastern United States': 0,
            'Mexico': 0, 'Venezuela': 0, 'Brazil': 0, 'Peru': 0, 'Argentina': 0,
            'North Africa': 0, 'Egypt': 0, 'East Africa': 0, 'Congo': 0, 'South Africa': 0,
            'Madagascar': 0, 'Iceland': 0, 'Scandinavia': 0, 'Great Britain': 0,
            'Northern Europe': 0, 'Western Europe': 0, 'Southern Europe': 0,
            'Ukraine': 0, 'Ural': 0, 'Siberia': 0, 'Yakutsk': 0, 'Kamchatka': 0,
            'Japan': 0, 'Mongolia': 0, 'Irkutsk': 0, 'China': 0, 'Siam': 0,
            'India': 0, 'Middle East': 0, 'Kazakhstan': 0, 'Indonesia': 0,
            'New Guinea': 0, 'Eastern Australia': 0, 'Western Australia': 0
        }
        self.regions_dict = {'North America': ['Alaska', 'Northwest territory', 'Greenland', 'Alberta',
                                          'Ontario', 'Quebec', 'Western United States',
                                          'Eastern United States', 'Mexico'],
                        'South America': ['Venezuela', 'Brazil', 'Peru', 'Argentina'],
                        'Africa': ['North Africa', 'Egypt', 'East Africa',
                                   'Congo', 'South Africa', 'Madagascar'],
                        'Europe': ['Iceland', 'Scandinavia', 'Ukraine', 'Northern Europe',
                                   'Western Europe', 'Southern Europe', 'Great Britain'],
                        'Asia': ['Ural', 'Siberia', 'Yakutsk', 'Kamchatka', 'Japan',
                                 'Irkutsk', 'Kazakhstan', 'Middle East', 'India', 'Siam',
                                 'China', 'Mongolia'],
                        'Oceania': ['Indonesia', 'New Guinea', 'Eastern Australia',
                                    'Western Australia']}

        self.regions_bonus_dict = {'North America': 5, 'South America': 2, 'Africa': 3,
                              'Europe': 5, 'Asia': 7, 'Oceania': 2}

        self.regions_country_count_dict = {'North America': 9, 'South America': 4, 'Africa': 6,
                              'Europe': 7, 'Asia': 12, 'Oceania': 4}

    def fill_defend_value_map(self):
        """Fill value map of which countries have highest priority to be defended"""

    def fill_attack_value_map(self):
        """Fill value map of which countries have highest priority to be attacked"""

    """EVERYTHING UNDER HERE IS JUST RANDOM AGENT CODE...."""

    def get_possible_moves(self, owned_countries, map):
        """Returns an array of all the possible moves the agent could make, where
        a move is (origin_country, destination_country, armies)"""
        possible_moves = []

        for country in list(owned_countries.keys()):
            current_neighbours = [n for n in map.map_graph.neighbors(country)]
            current_armies_count = owned_countries[str(country)]
            for neighbour in current_neighbours:
                for i in range(current_armies_count + 1):
                    possible_moves.append((str(country), str(neighbour), i))

        return possible_moves

    def remove_used_armies_from_pool(self, current_owned_countries, move):
        """Removes armies from a country based on a move having been selected.
        e.g. the move is (Iceland, Britain, 3) means removing 3 armies from Iceland.
        This is not done to the actual game, but just as a temporary counter to keep
        track of how many armies are left to play with in this particular turn"""
        country_to_be_altered = move[0]
        armies_to_deduct = move[2]
        current_owned_countries[str(country_to_be_altered)] -= armies_to_deduct
        return current_owned_countries

    def regions_owned_count(self, owned_countries):
        """Checks to see which regions on the map are owned completely"""

        owned_count  = {'North America': 0, 'South America': 0, 'Africa': 0,
         'Europe': 0, 'Asia': 0, 'Oceania': 0}
        owned_completely = []

        for owned_country in owned_countries:
            for region in self.regions_country_count_dict.keys():
                if str(owned_country) in self.regions_dict[str(region)]:
                    self.regions_country_count_dict[str(region)] -= 1
                    owned_count[str(region)] += 1

        for region in owned_count.keys():
            if owned_count[str(region)] == len(self.regions_dict[str(region)]):
                owned_completely.append(str(region))

        return owned_completely

    def choose_moves(self, map, colour, owned_countries, reinf_card_count):
        """Chooses a move based on game heuristics alone. The moves are
        returned in the format (origin_country, destination_country, army_count)"""
        current_owned_countries = owned_countries
        neighbouring_countries = []
        chosen_moves = []

        """if the agent has any reinforcement cards to play, play them all"""
        if reinf_card_count > 0:
            reinf_cards_played = reinf_card_count
        else:
            reinf_cards_played = 0

        for country in list(current_owned_countries.keys()):
            neighbouring_countries.append([n for n in map.map_graph.neighbors(country)])

            possible_moves = self.get_possible_moves(current_owned_countries, map)

            while len(possible_moves) > 0:
                possible_moves = self.get_possible_moves(current_owned_countries, map)
                if len(possible_moves) > 0:

                    """check if any neighbouring countries have opponent armies"""
                    for neighbouring_country in neighbouring_countries:
                        if map.get_colours_dict()[str(neighbouring_country)] != str(self.colour):
                            self.defend_value_map[str(country)] += 1
                            if str(neighbouring_country) not in self.enemy_countries:
                                self.enemy_countries.append(str(neighbouring_country))

                            """work out when an army can overwhelm a neighbouring country 
                                                in one turn, based on their max possible income"""

                            # TODO: need to account for the max possible armies that the opponent \\
                            # might be able to put into a country before the moves get made.

                            if map.get_armies_dict()[str(neighbouring_country)] > 0 :
                                if (map.get_armies_dict()[str(neighbouring_country)] * 1.5) < map.get_armies_dict()[str(country)]:
                                    self.overwhelming_move.append((str(country), str(neighbouring_country),
                                                                   str(map.get_armies_dict()[str(neighbouring_country)] * 1.5)))

                        """Check if neighbouring country has 0 armies"""
                        if map.get_armies_dict()[str(neighbouring_country)] == 0:
                            if str(neighbouring_country) not in self.empty_countries:
                                self.empty_countries.append(str(neighbouring_country))

        """If there are enemy owned countries bordering owned countries"""
        if len(self.enemy_countries) > 0:
            """If it is possible to totally overwhelm an enemy country"""
            if len(self.overwhelming_move) > 0:
                owned_completely = self.regions_owned_count(owned_countries)
                for region in self.regions_country_count_dict.keys():
                    """If an antire region can be won by taking a single country"""
                    if self.regions_country_count_dict[str(region)] == 1:
                        """Check if there is a possible overhwleming move for this country"""
                        for move in self.overwhelming_move:
                            if str(move[1]) in self.regions_dict[str(region)]:
                                """Add the move to the list of chosen moves"""
                                chosen_moves.append(move)










                    """If it is possible to prevent negative actions from countries in the critical list, 
                    then do this. prioritise based on whether friendlies own the entire region, and then
                    on the value of the region"""

                    """If there are armies left after dealing with priority and critical lists, or if they 
                    were both empty..."""

                    """if a neighbouring country has 0 armies and if there is an available army nearby, 
                                        send 1 army over to take that country"""

                    """Look at owned countries, and identify the closest attainable entire territory, and 
                    make moves to obtain it"""

        return chosen_moves, reinf_cards_played, owned_countries

    def allocate_armies(self, additional_armies, owned_countries):
        """Takes in a number of armies to be allocated, and randomly allocates
        them to countries. The returns the owned_countries dict"""
        print(str(self.colour) + ' owns these countries: ' + str(owned_countries))
        while additional_armies > 0:
            country = random.choice(list(owned_countries.keys()))
            print('Algorithm has chosen ' + str(country) + ' to be allocated an army')
            owned_countries[str(country)] += 1
            additional_armies -= 1

        print('after allocating, ' + str(self.colour) + ' owns these countries: ' + str(owned_countries))

        return owned_countries

    def consider_reinf_card(self, reinf_card_count):
        """Random agent always plays all reinforcement card immediately"""
        return reinf_card_count






