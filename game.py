import create_map
import controller
import networkx as nx
import matplotlib.pyplot as plt
import random

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
        self.map_graph = create_map.create_graph(False)
        self.player1 = controller.Controller('b', player1_algorithm)
        self.player2 = controller.Controller('r', player2_algorithm)
        self.colours = {
            'Alaska': 'k', 'Northwest territory': 'k', 'Greenland': 'k', 'Alberta': 'k',
            'Ontario': 'k', 'Quebec': 'k', 'Western United States': 'k', 'Eastern United States': 'k',
            'Mexico': 'k', 'Venezuela': 'k', 'Brazil': 'k', 'Peru': 'k', 'Argentina': 'k',
            'North Africa': 'k', 'Egypt': 'k', 'East Africa': 'k', 'Congo': 'k', 'South Africa': 'k',
            'Madagascar': 'k', 'Iceland': 'k', 'Scandinavia': 'k', 'Great Britain': 'k',
            'Northern Europe': 'k', 'Western Europe': 'k', 'Southern Europe': 'k',
            'Ukraine': 'k', 'Ural': 'k', 'Siberia': 'k', 'Yakutsk': 'k', 'Kamchatka': 'k',
            'Japan': 'k', 'Mongolia': 'k', 'Irkutsk': 'k', 'China': 'k', 'Siam': 'k',
            'India': 'k', 'Middle East': 'k', 'Kazakhstan': 'k', 'Indonesia': 'k',
            'New Guinea': 'k', 'Eastern Australia': 'k', 'Western Australia': 'k'
        }

    def change_colour(self, country, colour):
        """Changes the colour of a node on the map (colour will always be
        either 'b' for player1 or 'r' for player2)"""
        self.colours[str(country)] = str(colour)

    def get_colour(self, country):
        """Returns the colour of a particular country"""
        return self.colours[str(country)]

    def print_map(self):
        """Prints off the map"""
        colour_values = [self.colours.get(node, 0.25) for node in self.map_graph.nodes()]
        nx.draw(self.map_graph, nx.get_node_attributes(self.map_graph, 'pos'),
                node_color=colour_values, with_labels=False, node_size=100)
        plt.show()

    def random_starting_positions(self):
        """Picks 2 countries for each player as starting position, and
        changes the colour of these countries."""

        #TODO: need to add an army count for each country and set this to 4

        p1_start = 0
        p2_start = 0

        while p1_start != 2:
            pick = random.choice(list(self.colours.keys()))
            if self.colours[str(pick)] == 'k':
                self.change_colour(str(pick), 'b')
                self.player1.add_owned_county(str(pick))
                p1_start += 1

        while p2_start != 2:
            pick = random.choice(list(self.colours.keys()))
            if self.colours[str(pick)] == 'k':
                self.change_colour(str(pick), 'r')
                self.player2.add_owned_county(str(pick))
                p2_start += 1





