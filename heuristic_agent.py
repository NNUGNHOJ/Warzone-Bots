import random

class Heuristic_agent:
    """Uses game heuristics only"""

    def __init__(self, colour):
        self.colour = colour
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
                for i in range(current_armies_count):
                    possible_moves.append((str(country), str(neighbour), i + 1))

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

    def choose_moves(self, map, colour, owned_countries, reinf_card_count):
        """Chooses a random move based on the possible moves in the map. The moves are
        returned in the format (origin_country, destination_country, army_count)"""
        current_owned_countries = owned_countries
        neighbouring_countries = []
        chosen_moves = []

        """if the agent has any reinforcement cards to play, play them all"""
        if reinf_card_count > 0:
            reinf_cards_played = reinf_card_count
        else:
            reinf_cards_played = 0

        """Get all the countries neighbouring owned countries"""
        for country in list(current_owned_countries.keys()):
            neighbouring_countries.append([n for n in map.map_graph.neighbors(country)])

            possible_moves = self.get_possible_moves(current_owned_countries, map)

            while len(possible_moves) > 0:
                possible_moves = self.get_possible_moves(current_owned_countries, map)
                if len(possible_moves) > 0:
                    move = random.choice(possible_moves)
                    current_owned_countries = self.remove_used_armies_from_pool(current_owned_countries, move)
                    chosen_moves.append(move)

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




