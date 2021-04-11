import random

class Random_agent:
    """Picks moves at random"""

    def __init__(self, colour):
        self.colour = colour

    def choose_moves(self, map, colour, owned_countries, reinf_card_count):
        """Chooses a random move based on the possible moves in the map"""
        neighbouring_countries = []

        for country in list(owned_countries.keys()):
            neighbouring_countries.append([n for n in map.map_graph.neighbors(country)])

        print(neighbouring_countries)

