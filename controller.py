import random_agent
import math


class Controller:
    """A controller object represents a single player, with a
    pre-defined colour and algorithm (e.g. MCTS, RHEA, etc...)"""

    def __init__(self, colour, algorithm):
        self.colour = colour
        self.owned_countries = {}  # {'country_name': army count in this country}
        self.reinf_card_count = 0
        self.new_reinf_card = 0 # when new_reinf_card is 8 the player gets 1 new reinf card

        if algorithm == 'Random':
            self.algorithm = random_agent.Random_agent(colour)
        else:
            print("Only random agent has been implemented so far...")

    def get_colour(self):
        return self.colour

    def get_algorithm(self):
        return self.algorithm

    def get_owned_countries(self):
        return self.owned_countries

    def add_owned_country(self, country, armies):
        """Adds a country to the dict of countries owned by this player"""
        self.owned_countries[str(country)] = armies

    def remove_owned_country(self, country):
        """Removes a country to the dict of countries owned by this player"""
        del self.owned_countries[str(country)]

    def set_owned_country_armies(self, country, armies):
        """Change the number of armies in an owned country"""
        self.owned_countries[str(country)] = armies

    def get_reinf_card_count(self):
        """Return number of reinforcement cards the player has"""
        return self.reinf_card_count

    def set_reinf_card_count(self, count):
        """Changes the number of reinforcement cards the player has"""
        self.reinf_card_count = count

    def check_for_new_reinf_card(self):
        """Checks if the player is due a new reinforcement card, if so it
        returns the total number, and sets reinf"""
        if self.new_reinf_card / 6 >= 1:
            number_of_new_reinf_cards = math.floor(self.new_reinf_card / 8)
            self.new_reinf_card = self.new_reinf_card - (8 * number_of_new_reinf_cards)
            return number_of_new_reinf_cards
        else:
            return 0

    def choose_moves(self, map):
        """Takes in a game state and chooses moves to make."""
        moves = self.algorithm.choose_moves(map, self.colour, self.owned_countries, self.reinf_card_count)
        return moves

    def consider_reinf_card(self, map):
        """Decide whether to play a reinforcement card or not. Returns the
        number fo reinforcement cards being played this turn."""
        reinf_cards_to_play = self.algorithm.consider_reinf_card(self.reinf_card_count)
        return reinf_cards_to_play

    def allocate_armies(self, additional_armies):
        self.owned_countries = self.algorithm.allocate_armies(additional_armies, self.owned_countries)

