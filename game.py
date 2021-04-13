import create_map
import controller
import networkx as nx
import matplotlib.pyplot as plt
import random
import map


class Game:
    """A single Game object is a single game, with a corresponding
    set of map states (one for each turn)"""

    def __init__(self, player1_algorithm, player2_algorithm):
        self.map_graph = map.Map()
        self.player1 = controller.Controller('b', player1_algorithm)
        self.player2 = controller.Controller('r', player2_algorithm)

        # game stats
        self.turn_count = 0
        self.player1_territories = [2]
        self.player2_territories = [2]
        self.player1_armies = [8]
        self.player2_armies = [8]
        self.player1_armies_lost = [0]
        self.player2_armies_lost = [0]
        self.player1_armies_killed = [0]
        self.player2_armies_killed = [0]
        self.player1_reinf_cards_played = [0]
        self.player2_reinf_cards_played = [0]

    def random_starting_positions(self):
        """Picks 2 random countries for each player as starting position, and
        changes the colour of these countries on the map graph, as well giving
        each new country 4 armies.."""

        p1_start = 0
        p2_start = 0

        while p1_start != 2:
            pick = self.map_graph.get_random_country()

            if self.map_graph.get_colour(str(pick)) == 'k':
                self.map_graph.change_colour(str(pick), 'b')
                self.player1.add_owned_country(str(pick), 4)
                print('player 1 has been given: ' + str(pick))
                print('player 1 countries: ' + str(self.player1.get_owned_countries()))
                self.map_graph.set_army_count(str(pick), 4)
                p1_start += 1

        while p2_start != 2:
            pick = self.map_graph.get_random_country()

            if self.map_graph.get_colour(str(pick)) == 'k':
                self.map_graph.change_colour(str(pick), 'r')
                self.player2.add_owned_country(str(pick), 4)
                print('player 2 has been given: ' + str(pick))
                print('player 2 countries: ' + str(self.player2.get_owned_countries()))
                self.map_graph.set_army_count(str(pick), 4)
                p2_start += 1
        return

    def print_map(self):
        """Prints off the map belonging to a game object"""
        self.map_graph.print_map()

    def get_moves(self):
        """Allows both players to choose the actions to take for their move, note that
        the moves aren't made yet, as the order in which they're done matters. So player1
        might want to move x armies from one place to another, but player2 has already
        killed some of that army. Remember: each move is made alternatively one player
        at a time."""

        player1_moves, reinf_card_played1 = self.player1.choose_moves(self.map_graph)
        player2_moves, reinf_card_played2 = self.player2.choose_moves(self.map_graph)

        return player1_moves, reinf_card_played1, player2_moves, reinf_card_played2

    def make_move(self, move, colour):
        """Takes a single move and performs it on the map graph"""
        #TODO: actually make a move on the map

    def total_armies_to_allocate(self, player, reinf_cards_played):
        """Works out how many armies a player has to allocate in this turn. This
        includes playing reinforcements cards, or owning entire regions. Each turn
        automatically gives the players 5 resources."""
        total_armies = 5
        total_armies += reinf_cards_played * 4
        region_dict = self.map_graph.regions_dict
        countries_owned_by_player = player.get_owned_countries()

        for region in region_dict.keys():
            total_countries_in_region = len(region)
            player_countries_count_in_region = 0
            for country in region:
                if str(country) in countries_owned_by_player.keys():
                    player_countries_count_in_region += 1
            """If the player owns all the countries in a region, they get a bonus"""
            if player_countries_count_in_region == total_countries_in_region:
                regions_bonus_dict = self.map_graph.get_bonus_dict()
                bonus = regions_bonus_dict[str(region)]
                total_armies += bonus
        return total_armies

    def adjust_map(self, player1_owned_countries, player2_owned_countries):
        """Changes the map to reflect the owned countries and army counts as per the players"""
        for country in player1_owned_countries.keys():
            self.map_graph.change_colour(str(country), 'b')
            self.map_graph.set_army_count(str(country), player1_owned_countries[str(country)])

        for country in player2_owned_countries.keys():
            self.map_graph.change_colour(str(country), 'r')
            self.map_graph.set_army_count(str(country), player1_owned_countries[str(country)])

    def allocate_armies(self, player1_additional_armies, player2_additional_armies):
        self.player1.allocate_armies(player1_additional_armies)
        self.player2.allocate_armies(player2_additional_armies)
        self.adjust_map(self.player1.get_owned_countries(), self.player2.get_owned_countries())


    def perform_moves_in_order(self):
        """Takes an array of moves, and performs them in alternating order. Effectively performing 1 turn"""
        #TODO: we may need to balance which player's move gets made first

        """Check if players want to play any reinforcement cards"""


        """Get list of moves to make for each player"""
        player1_moves, reinf_card_played1, player2_moves, reinf_card_played2 = self.get_moves()

        """Calculate how many new armies each player gets this turn"""
        player1_additional_armies = self.total_armies_to_allocate(self.player1, reinf_card_played1)
        player2_additional_armies = self.total_armies_to_allocate(self.player2, reinf_card_played2)

        """Allow both players to allocate their new armies"""
        self.allocate_armies(player1_additional_armies, player2_additional_armies)

        """Adjust the Game object's map to reflect the countries and army countrs of the players"""
        self.adjust_map(self.player1.get_owned_countries(), self.player2.get_owned_countries())



        """"""

        """adjust statistic for both players"""
        self.player1_reinf_cards_played.append(reinf_card_played1)
        self.player2_reinf_cards_played.append(reinf_card_played2)
        self.player1_armies.append(self.player1_armies[len(self.player1_armies) - 1] + player1_additional_armies)
        self.player2_armies.append(self.player2_armies[len(self.player2_armies) - 1] + player2_additional_armies)

        count = 0
        player1_moves_made_count = 0
        player2_moves_made_count = 0

        while len(player1_moves) != 0 or len(player2_moves) != 0:
            count += 1
            if count % 2 == 0 and len(player1_moves) != 0:
                self.make_move(player1_moves[player1_moves_made_count], 'b')
                player1_moves_made_count += 1
            elif count % 2 == 1 and len(player2_moves) != 0:
                self.make_move(player2_moves[player2_moves_made_count], 'r')
                player2_moves_made_count += 1