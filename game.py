import create_map
import controller
import networkx as nx
import matplotlib.pyplot as plt
import random
import map


class Game:
    """A single Game object is a single game, with a corresponding
    set of map states (one for each turn)"""

    #game stats
    turn_count = 0
    player1_territories = [2]
    player2_territories = [2]
    player1_armies = [8]
    player2_armies = [8]
    player1_armies_lost = [0]
    player2_armies_lost = [0]
    player1_armies_killed = [0]
    player2_armies_killed = [0]
    player1_reinf_cards_played = [0]
    player2_reinf_cards_played = [0]

    def __init__(self, player1_algorithm, player2_algorithm):
        self.map_graph = map.Map()
        self.player1 = controller.Controller('b', player1_algorithm)
        self.player2 = controller.Controller('r', player2_algorithm)

    def random_starting_positions(self):
        """Picks 2 countries for each player as starting position, and
        changes the colour of these countries, and place the initial
        4 armies in each country."""

        p1_start = 0
        p2_start = 0

        while p1_start != 2:
            pick = self.map_graph.get_random_country()

            if self.map_graph.get_colour(str(pick)) == 'k':
                self.map_graph.change_colour(str(pick), 'b')
                self.player1.add_owned_county(str(pick), 4) #sets army count for the player
                print('player 1 has been given: ' + str(pick))
                self.map_graph.set_army_count(str(pick), 4) #sets army count for the map
                p1_start += 1

        while p2_start != 2:
            pick = self.map_graph.get_random_country()

            if self.map_graph.get_colour(str(pick)) == 'k':
                self.map_graph.change_colour(str(pick), 'r')
                self.player2.add_owned_county(str(pick), 4) #sets army count for the player
                print('player 2 has been given: ' + str(pick))
                self.map_graph.set_army_count(str(pick), 4) #sets army count for the map
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

        player1_moves = self.player1.choose_moves(self.map_graph)
        player2_moves = self.player2.choose_moves(self.map_graph)

        return player1_moves, player2_moves

    def perform_moves_in_order(self, player1_moves, player2_moves):
        """Takes an array of moves, and performs them in alternating order."""