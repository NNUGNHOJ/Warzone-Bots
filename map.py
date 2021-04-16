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

    regions_bonus_dict = {'North America': 5, 'South America': 2, 'Africa': 3,
                    'Europe': 5, 'Asia': 7, 'Oceania': 2}

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
            'Alaska': 2, 'Northwest territory': 2, 'Greenland': 2, 'Alberta': 2,
            'Ontario': 2, 'Quebec': 2, 'Western United States': 2, 'Eastern United States': 2,
            'Mexico': 2, 'Venezuela': 2, 'Brazil': 2, 'Peru': 2, 'Argentina': 2,
            'North Africa': 2, 'Egypt': 2, 'East Africa': 2, 'Congo': 2, 'South Africa': 2,
            'Madagascar': 2, 'Iceland': 2, 'Scandinavia': 2, 'Great Britain': 2,
            'Northern Europe': 2, 'Western Europe': 2, 'Southern Europe': 2,
            'Ukraine': 2, 'Ural': 2, 'Siberia': 2, 'Yakutsk': 2, 'Kamchatka': 2,
            'Japan': 2, 'Mongolia': 2, 'Irkutsk': 2, 'China': 2, 'Siam': 2,
            'India': 2, 'Middle East': 2, 'Kazakhstan': 0, 'Indonesia': 2,
            'New Guinea': 2, 'Eastern Australia': 2, 'Western Australia': 2
        }

    def get_colours_dict(self):
        """Return a dict with the countries and their colours"""
        return self.colours

    def get_armies_dict(self):
        """Return a dict with the countries and their army counts"""
        return self.armies

    def get_bonus_dict(self):
        """Returns dict with the bonus armies from each region"""
        return self.regions_bonus_dict

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
        return

    def print_map(self):
        """Prints off the map"""
        colour_values = [self.colours.get(node, 0.25) for node in self.map_graph.nodes()]
        nx.draw(self.map_graph, nx.get_node_attributes(self.map_graph, 'pos'),
                node_color=colour_values, with_labels=False, node_size=100)
        plt.show()

    def get_turn_statistics(self):
        player1_countries = []
        player2_countries = []

        for key, value in self.colours.items():
            if value == 'b':
                army_in_country = self.armies[str(key)]
                player1_countries.append((str(key), army_in_country))

            if value == 'r':
                army_in_country = self.armies[str(key)]
                player2_countries.append((str(key), army_in_country))

        return player1_countries, player2_countries, self.armies.keys()





