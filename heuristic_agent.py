import random
from numpy.random import choice

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

    def get_possible_moves(self, owned_countries, map):
        """Returns an array of all the possible moves the agent could make, where
        a move is (origin_country, destination_country, armies)"""
        possible_moves = []

        for country in list(owned_countries.keys()):
            current_neighbours = [n for n in map.map_graph.neighbors(country)]
            current_armies_count = owned_countries[str(country)]
            for neighbour in current_neighbours:
                for i in range(int(current_armies_count + 1)):
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

    def play_all_reinf_cards(self, reinf_card_count):
        """if the agent has any reinforcement cards to play, play them all"""
        if reinf_card_count > 0:
            reinf_cards_played = reinf_card_count
        else:
            reinf_cards_played = 0

        return reinf_cards_played

    def choose_moves(self, map, colour, owned_countries, reinf_card_count):
        """Chooses a move based on game heuristics alone. The moves are
        returned in the format (origin_country, destination_country, army_count)"""
        current_owned_countries = owned_countries
        neighbouring_countries = []
        chosen_moves = []

        reinf_cards_played = self.play_all_reinf_cards(reinf_card_count)

        for country in list(current_owned_countries.keys()):
            neighbouring_countries.append([n for n in map.map_graph.neighbors(country)])

            possible_moves = self.get_possible_moves(current_owned_countries, map)
            if len(possible_moves) > 0:

                """check if any neighbouring countries have opponent armies"""
                for neighbouring_country in neighbouring_countries[0]:
                    if map.get_colours_dict()[str(neighbouring_country)] != str(self.colour):
                        self.defend_value_map[str(country)] += 1

                        if str(neighbouring_country) not in self.enemy_countries:
                            self.enemy_countries.append(str(neighbouring_country))

                        """work out when an army can overwhelm a neighbouring country 
                                            in one turn, based on their max possible income"""

                        """If neighbouring country has armies in it"""
                        if map.get_armies_dict()[str(neighbouring_country)] > 0:
                            """If friendly army count is greater than 1.5 * enemy army count, add overwhelming move"""
                            if (map.get_armies_dict()[str(neighbouring_country)] * 1.5) < map.get_armies_dict()[str(country)]:
                                self.overwhelming_move.append((str(country), str(neighbouring_country),
                                                               round(map.get_armies_dict()[str(neighbouring_country)] * 1.5)))

                    """Check if neighbouring country has 0 armies"""
                    if map.get_armies_dict()[str(neighbouring_country)] == 0:
                        if str(neighbouring_country) not in self.empty_countries:
                            self.empty_countries.append((str(country), str(neighbouring_country)))

            neighbouring_countries.clear()

        """If there are enemy owned countries bordering owned countries"""
        if len(self.enemy_countries) > 0:
            """If it is possible to totally overwhelm an enemy country"""
            if len(self.overwhelming_move) > 0:
                owned_completely = self.regions_owned_count(owned_countries)
                for region in self.regions_country_count_dict.keys():
                    """If an entire region can be won by taking a single country"""
                    if self.regions_country_count_dict[str(region)] == 1:
                        """Check if there is a possible overwhelming move for this country"""
                        for move in self.overwhelming_move:
                            if str(move[1]) in self.regions_dict[str(region)]:
                                """Add the move to the list of chosen moves"""
                                chosen_moves.append(move)
                                self.remove_used_armies_from_pool(current_owned_countries, move)

        for empty_country_moves in self.empty_countries:
            """If owned country has any armies in it"""
            if current_owned_countries[str(empty_country_moves[0])] > 0:
                move = (str(empty_country_moves[0]), str(empty_country_moves[1]), 1)
                chosen_moves.append(move)
                self.remove_used_armies_from_pool(current_owned_countries, move)
                self.empty_countries.remove(empty_country_moves)

        possible_moves = self.get_possible_moves(current_owned_countries, map)

        while len(possible_moves) > 0 and len(self.overwhelming_move) > 0:
            possible_moves = self.get_possible_moves(current_owned_countries, map)
            move = self.overwhelming_move[0]
            self.overwhelming_move.remove(move)
            self.remove_used_armies_from_pool(current_owned_countries, move)
            chosen_moves.append(move)

        """Reset known info, will be reconstructed next turn"""
        self.overwhelming_move.clear()
        self.enemy_countries.clear()
        self.empty_countries.clear()
        self.defend_value_map = dict.fromkeys(self.defend_value_map, 0)

        return chosen_moves, reinf_cards_played, owned_countries


    def allocate_armies(self, additional_armies, owned_countries, map):
        """Takes in a number of armies to be allocated, works out which countries most
         need additional armies. Then allocates armies based on a probability distribution,
         where countries that need armies are more likely to get given them. Then returns
         the owned_countries dict"""

        current_owned_countries = owned_countries
        neighbouring_countries = []
        placement_probability_dict = owned_countries

        """set initial probabilities to 0"""
        placement_probability_dict = dict.fromkeys(placement_probability_dict, 0)

        """For each country, work out how many armies to give it"""
        for country in list(current_owned_countries.keys()):
            neighbouring_countries.append([n for n in map.map_graph.neighbors(country)])

            """check if any neighbouring countries have opponent armies"""
            for neighbouring_country in neighbouring_countries[0]:
                """If neighbour colour not the same as player colour"""
                if map.get_colours_dict()[str(neighbouring_country)] != str(self.colour):
                    """If neighbouring country isn't owned by anyone, just add 1"""
                    if map.get_colours_dict()[str(neighbouring_country)] == 'b':
                        placement_probability_dict[str(country)] += 2
                    else:
                        """If country already has an overwhelming number of armies, dont bother adding more, save 
                        them for some other country"""
                        if (map.get_armies_dict()[str(neighbouring_country)] * 1.5) <= map.get_armies_dict()[str(country)]:
                            placement_probability_dict[str(country)] += 1
                        else:
                            """Add probability based on how many armies are in that neighbouring country"""
                            placement_probability_dict[str(country)] += 10
            neighbouring_countries = []

        """Allocate the armies based on the collected probability distribution"""

        """Turn values into probabilities of allocating"""
        total = 0
        list_of_candidates = [*placement_probability_dict]
        probability_distribution = []

        for key, item in placement_probability_dict.items():
            total += item

        for key, item in placement_probability_dict.items():
            if total > 0:
                placement_probability_dict[str(key)] = item / total
                probability_distribution.append(item / total)
            else:
                print('total is 0')
                break

        """Choose countries 'randomly' but weighted based on probability distribution"""
        chosen_countries = random.choices(population=list_of_candidates,
                                          weights=probability_distribution,
                                          k=additional_armies)

        """Allocate the chosen countries"""
        for country in chosen_countries:
            owned_countries[str(country)] += 1

        return owned_countries

    def consider_reinf_card(self, reinf_card_count):
        """Heuristic agent always plays all reinforcement card immediately"""
        return reinf_card_count






