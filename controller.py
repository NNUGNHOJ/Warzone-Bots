import random_agent


class Controller:
    """A controller object represents a single player, with a
    pre-defined colour and algorithm (e.g. MCTS, RHEA, etc...)"""

    owned_countries = {} # {'country_name': army count in this country}
    reinf_card_count = 0

    def __init__(self, colour, algorithm):
        self.colour = colour
        if algorithm == 'Random':
            self.algorithm = random_agent.Random_agent(colour)
        else:
            print("Only random agent has been implemented so far...")

    def get_colour(self):
        return self.colour

    def get_algorithm(self):
        return self.algorithm

    def add_owned_county(self, country, armies):
        """Adds a country to the dict of coutnries owned by this player"""
        self.owned_countries[str(country)] = armies

    def remove_owned_country(self, country):
        """Removes a country to the dict of coutnries owned by this player"""
        del self.owned_countries[str(country)]

    def choose_moves(self, map):
        """Takes in a game state and chooses moves to make."""
        self.algorithm.choose_moves(map, self.colour, self.owned_countries, self.reinf_card_count)
