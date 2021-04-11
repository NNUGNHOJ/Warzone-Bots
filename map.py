import networkx as nx
import matplotlib.pyplot as plt
import create_map
import random


class Map:
    """Map object, keeps track of the current state of the map"""

    regions_dict = {'North America': ['Alaska', 'Northwest territory', 'Greenland', 'Alberta',
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

    def __init__(self):
        self.map_graph = create_map.create_graph(False)
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
        self.armies = {
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

    def get_colours_dict(self):
        """Return a dict with the countries and their colours"""
        return self.colours

    def get_random_country(self):
        """Return countries on the map"""
        return random.choice(list(self.colours.keys()))

    def change_colour(self, country, colour):
        """Changes the colour of a node on the map (colour will always be
        either 'b' for player1 or 'r' for player2)"""
        self.colours[str(country)] = str(colour)

    def get_colour(self, country):
        """Returns the colour of a particular country"""
        return self.colours[str(country)]

    def set_army_count(self, country, army_count):
        """Changes the army count of a country"""
        self.armies[str(country)] = army_count

    def print_map(self):
        """Prints off the map"""
        colour_values = [self.colours.get(node, 0.25) for node in self.map_graph.nodes()]
        nx.draw(self.map_graph, nx.get_node_attributes(self.map_graph, 'pos'),
                node_color=colour_values, with_labels=False, node_size=100)
        plt.show()




