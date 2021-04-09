


class Controller:
    """A controller object represents a single player, with a
    pre-defined colour and algorithm (e.g. MCTS, RHEA, etc...)"""

    owned_countries = []
    reinf_card_count = 0

    def __init__(self, colour, algorithm):
        self.colour = colour
        self.algorithm = algorithm

    def get_colour(self):
        return self.colour

    def get_algorithm(self):
        return self.algorithm
    
    def add_owned_county(self, country):
        self.owned_countries.append(str(country))
