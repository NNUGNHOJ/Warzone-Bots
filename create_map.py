import networkx as nx
import matplotlib.pyplot as plt

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

def create_graph(print):
    """Creates a network for the game map and returns thw graph. When print is True,
    it will print off the network with colours representing the regions."""

    G = nx.Graph()

    #North America
    G.add_node('Alaska', region='North America', pos=(0.5, 8.5))
    G.add_node('Northwest territory', region='North America', pos=(3.5, 8.5))
    G.add_node('Greenland', region='North America', pos=(7.1, 10.5))
    G.add_node('Alberta', region='North America', pos=(3, 7.5))
    G.add_node('Ontario', region='North America', pos=(4, 7.5))
    G.add_node('Quebec', region='North America', pos=(5.5, 7.4))
    G.add_node('Western United States', region='North America', pos=(3.5, 6.5))
    G.add_node('Eastern United States', region='North America', pos=(4.5, 6.3))
    G.add_node('Mexico', region='North America', pos=(3, 5))

    G.add_edge('Alaska', 'Northwest territory')
    G.add_edge('Alaska', 'Alberta')
    G.add_edge('Alberta', 'Ontario')
    G.add_edge('Alberta', 'Western United States')
    G.add_edge('Alberta', 'Northwest territory')
    G.add_edge('Ontario', 'Greenland')
    G.add_edge('Ontario', 'Quebec')
    G.add_edge('Ontario', 'Eastern United States')
    G.add_edge('Northwest territory', 'Greenland')
    G.add_edge('Northwest territory', 'Ontario')
    G.add_edge('Western United States', 'Ontario')
    G.add_edge('Western United States', 'Eastern United States')
    G.add_edge('Quebec', 'Eastern United States')
    G.add_edge('Quebec', 'Greenland')
    G.add_edge('Mexico', 'Eastern United States')
    G.add_edge('Mexico', 'Western United States')

    #South America
    G.add_node('Venezuela', region='South America', pos=(4.5, 4.4))
    G.add_node('Brazil', region='South America', pos=(5.8, 3.5))
    G.add_node('Peru', region='South America', pos=(4.5, 3.2))
    G.add_node('Argentina', region='South America', pos=(5, 2.3))

    G.add_edge('Mexico', 'Venezuela')
    G.add_edge('Brazil', 'Venezuela')
    G.add_edge('Peru', 'Venezuela')
    G.add_edge('Peru', 'Brazil')
    G.add_edge('Peru', 'Argentina')
    G.add_edge('Brazil', 'Argentina')

    #Africa
    G.add_node('North Africa', region='Africa', pos=(8, 5))
    G.add_node('Egypt', region='Africa', pos=(9, 5.5))
    G.add_node('East Africa', region='Africa', pos=(11, 4.2))
    G.add_node('Congo', region='Africa', pos=(10, 4))
    G.add_node('South Africa', region='Africa', pos=(10.1, 3))
    G.add_node('Madagascar', region='Africa', pos=(11.2, 3))

    G.add_edge('North Africa', 'Brazil')
    G.add_edge('North Africa', 'Egypt')
    G.add_edge('North Africa', 'East Africa')
    G.add_edge('North Africa', 'Congo')
    G.add_edge('East Africa', 'Congo')
    G.add_edge('East Africa', 'Egypt')
    G.add_edge('South Africa', 'Congo')
    G.add_edge('South Africa', 'Madagascar')
    G.add_edge('East Africa', 'Madagascar')
    G.add_edge('East Africa', 'South Africa')

    #Europe
    G.add_node('Iceland', region='Europe', pos=(7.1, 8.5))
    G.add_node('Scandinavia', region='Europe', pos=(9, 8.5))
    G.add_node('Great Britain', region='Europe', pos=(8, 7.5))
    G.add_node('Northern Europe', region='Europe', pos=(8.9, 7.3))
    G.add_node('Western Europe', region='Europe', pos=(7.9, 6))
    G.add_node('Southern Europe', region='Europe', pos=(9.2, 6.5))
    G.add_node('Ukraine', region='Europe', pos=(10, 8))

    G.add_edge('Greenland', 'Iceland')
    G.add_edge('Scandinavia', 'Iceland')
    G.add_edge('Great Britain', 'Iceland')
    G.add_edge('Great Britain', 'Western Europe')
    G.add_edge('Great Britain', 'Northern Europe')
    G.add_edge('Great Britain', 'Scandinavia')
    G.add_edge('Ukraine', 'Scandinavia')
    G.add_edge('Ukraine', 'Northern Europe')
    G.add_edge('Ukraine', 'Southern Europe')
    G.add_edge('Western Europe', 'Southern Europe')
    G.add_edge('Northern Europe', 'Southern Europe')
    G.add_edge('Western Europe', 'Northern Europe')
    G.add_edge('Western Europe', 'North Africa')
    G.add_edge('North Africa', 'Southern Europe')
    G.add_edge('Egypt', 'Southern Europe')

    #Asia
    G.add_node('Ural', region='Asia', pos=(11.5, 8))
    G.add_node('Siberia', region='Asia', pos=(12.9, 8.4))
    G.add_node('Yakutsk', region='Asia', pos=(14.3, 8.5))
    G.add_node('Kamchatka', region='Asia', pos=(16.1, 8.5))
    G.add_node('Japan', region='Asia', pos=(15, 6))
    G.add_node('Mongolia', region='Asia', pos=(14, 6.5))
    G.add_node('Irkutsk', region='Asia', pos=(13.6, 7.7))
    G.add_node('China', region='Asia', pos=(13, 5.9))
    G.add_node('Siam', region='Asia', pos=(13.1, 4.8))
    G.add_node('India', region='Asia', pos=(12, 5.1))
    G.add_node('Middle East', region='Asia', pos=(10.3, 5.8))
    G.add_node('Kazakhstan', region='Asia', pos=(11.4, 6.6))

    G.add_edge('Ural', 'Ukraine')
    G.add_edge('Ural', 'Siberia')
    G.add_edge('Ural', 'China')
    G.add_edge('Ural', 'Kazakhstan')
    G.add_edge('Siberia', 'Yakutsk')
    G.add_edge('Siberia', 'China')
    G.add_edge('Siberia', 'Mongolia')
    G.add_edge('Siberia', 'Irkutsk')
    G.add_edge('Kamchatka', 'Yakutsk')
    G.add_edge('Irkutsk', 'Yakutsk')
    G.add_edge('Kamchatka', 'Japan')
    G.add_edge('Kamchatka', 'Mongolia')
    G.add_edge('Kamchatka', 'Irkutsk')
    G.add_edge('Mongolia', 'Japan')
    G.add_edge('Irkutsk', 'Mongolia')
    G.add_edge('China', 'Mongolia')
    G.add_edge('China', 'Siam')
    G.add_edge('China', 'India')
    G.add_edge('China', 'Kazakhstan')
    G.add_edge('Middle East', 'India')
    G.add_edge('Kazakhstan', 'India')
    G.add_edge('Middle East', 'East Africa')
    G.add_edge('Middle East', 'Egypt')
    G.add_edge('Middle East', 'Southern Europe')
    G.add_edge('Middle East', 'Ukraine')
    G.add_edge('Ukraine', 'Kazakhstan')
    G.add_edge('India', 'Kazakhstan')
    G.add_edge('India', 'Siam')

    #Oceania
    G.add_node('Indonesia', region='Oceania', pos=(13.8, 4))
    G.add_node('New Guinea', region='Oceania', pos=(15.2, 3.8))
    G.add_node('Eastern Australia', region='Oceania', pos=(15.3, 2.6))
    G.add_node('Western Australia', region='Oceania', pos=(14.4, 2.7))

    G.add_edge('Indonesia', 'Siam')
    G.add_edge('New Guinea', 'Siam')
    G.add_edge('New Guinea', 'Indonesia')
    G.add_edge('Western Australia', 'Siam')
    G.add_edge('New Guinea', 'Western Australia')
    G.add_edge('New Guinea', 'Eastern Australia')
    G.add_edge('Western Australia', 'Eastern Australia')

    G.add_edge('Alaska', 'Kamchatka')

    colours = {
        'Alaska': 'r', 'Northwest territory': 'r', 'Greenland': 'r', 'Alberta': 'r',
        'Ontario': 'r', 'Quebec': 'r', 'Western United States': 'r', 'Eastern United States': 'r',
        'Mexico': 'r', 'Venezuela': 'b', 'Brazil': 'b', 'Peru': 'b', 'Argentina': 'b',
        'North Africa': 'g', 'Egypt': 'g', 'East Africa': 'g', 'Congo': 'g', 'South Africa': 'g',
        'Madagascar': 'g', 'Iceland': 'c', 'Scandinavia': 'c', 'Great Britain': 'c',
        'Northern Europe': 'c', 'Western Europe': 'c', 'Southern Europe': 'c', 'Ukraine': 'c',
        'Ural': 'm', 'Siberia': 'm', 'Yakutsk': 'm', 'Kamchatka': 'm', 'Japan': 'm',
        'Mongolia': 'm', 'Irkutsk': 'm', 'China': 'm', 'Siam': 'm', 'India': 'm',
        'Middle East': 'm', 'Kazakhstan': 'm', 'Indonesia': 'y', 'New Guinea': 'y',
        'Eastern Australia': 'y', 'Western Australia': 'y'
    }

    colour_values = [colours.get(node, 0.25) for node in G.nodes()]

    if print:
        nx.draw(G, nx.get_node_attributes(G, 'pos'), node_color=colour_values, with_labels=True, node_size=100)
        plt.show()

    return G


