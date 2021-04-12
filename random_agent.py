import random

class Random_agent:
    """Picks moves at random"""

    def __init__(self, colour):
        self.colour = colour

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

    def remove_used_armies_from_pool(self, current_owned_countries, move):
        """Removes armies from a country based on a move having been selected.
        e.g. the move is (Iceland, Britain, 3) means moving 3 armies from Iceland
        to Britain. In this case we have to remove 3 armies from Iceland"""
        country_to_be_altered = move[0]
        armies_to_deduct = move[2]
        current_owned_countries[str(country_to_be_altered)] -= armies_to_deduct
        return current_owned_countries

    def assign_new_armies_to_countries(self, armies, owned_countries, reinf_card_count):
        """Before making moves, agent needs to assign all their new armies to owned coutnries.
        If the agent has a reinforcement card, they can play it, in order to get an extra 4
        new armies to assign. The random agent always plays the reinforcement card immediately """
        #TODO: play reinforcement card
        #TODO: assign armies randomly
        return

    def choose_moves(self, map, colour, owned_countries, reinf_card_count):
        """Chooses a random move based on the possible moves in the map. The moves are
        returned in the format (origin_country, destination_country, army_count)"""
        current_owned_countries = owned_countries
        neighbouring_countries = []
        chosen_moves = []

        #if the agent has any reinforcement cards to play, play them all
        if reinf_card_count > 0:
            reinf_cards_played = reinf_card_count
            reinf_card_count = 0

        """Get all the countries neighbouring owned countries"""
        for country in list(current_owned_countries.keys()):
            neighbouring_countries.append([n for n in map.map_graph.neighbors(country)])

            possible_moves = self.get_possible_moves(owned_countries, map)

            while len(possible_moves) > 0:
                possible_moves = self.get_possible_moves(owned_countries, map)
                if len(possible_moves) > 0:
                    move = random.choice(possible_moves)
                    current_owned_countries = self.remove_used_armies_from_pool(current_owned_countries, move)
                    chosen_moves.append(move)

        return chosen_moves, reinf_cards_played




