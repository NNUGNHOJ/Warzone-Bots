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
        self.player1_armies = [13]
        self.player2_armies = [13]
        self.player1_armies_lost = [0]
        self.player2_armies_lost = [0]
        self.player1_armies_killed = [0]
        self.player2_armies_killed = [0]
        self.player1_reinf_cards_played = [0]
        self.player2_reinf_cards_played = [0]

    def get_map(self):
        """Returns the map object of this game"""
        return self.map_graph

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
                self.map_graph.set_army_count(str(pick), 4)
                p1_start += 1

        while p2_start != 2:
            pick = self.map_graph.get_random_country()

            if self.map_graph.get_colour(str(pick)) == 'k':
                self.map_graph.change_colour(str(pick), 'r')
                self.player2.add_owned_country(str(pick), 4)
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

        player1_moves, player1_reinf_cards_played = self.player1.choose_moves(self.map_graph)
        player2_moves, player2_reinf_cards_played = self.player2.choose_moves(self.map_graph)

        return player1_moves, player2_moves

    def make_move(self, move, colour):
        """Takes a single move and performs it on the map graph, a move consists
        of (origin_country, destination_country, armies_to_move)"""

        if str(colour) == 'b':
            print('player 1 about to make a move')
            attacking_player = self.player1
            """If destination_country isn't owned by either player"""
            if self.map_graph.get_colours_dict()[str(move[1])] == 'k':
                defending_player = None
            else:
                defending_player = self.player2

        else:
            print('player 2 about to make a move')
            attacking_player = self.player2
            """destination_country isn't owned by either player"""
            if self.map_graph.get_colours_dict()[str(move[1])] == 'k':
                defending_player = None
            else:
                defending_player = self.player1

        """Check that the player still owns the origin_country, if it does not, 
        then return without making the move."""
        if self.map_graph.get_colours_dict()[str(move[0])] != str(colour):
            print('Player making move does not own the destination country...')
            return

        """Check if the origin country still has all the armies the move wants to
        utilise"""

        """If the origin_country does not have as many armies as the move
        requires, then just use however many armies there are left."""
        if self.map_graph.get_armies_dict()[str(move[0])] >= move[2]:
            attacking_player_armies = move[2]
        else:
            attacking_player_armies = self.map_graph.get_armies_dict()[str(move[0])]

        """If the same player owns both countries, just transfer the armies"""
        if self.map_graph.get_colours_dict()[move[0]] == self.map_graph.get_colours_dict()[move[1]]:
            origin_army_count = self.map_graph.get_armies_dict()[move[0]]
            destination_army_count = self.map_graph.get_armies_dict()[move[1]]

            self.map_graph.set_army_count(str(move[0]), (origin_army_count - attacking_player_armies))
            self.map_graph.set_army_count(str(move[1]), (destination_army_count + attacking_player_armies))
            attacking_player.add_owned_country(str(move[0]), (origin_army_count - attacking_player_armies))
            attacking_player.add_owned_country(str(move[1]), (destination_army_count + attacking_player_armies))
            print(str(attacking_player.get_colour()) + ' was attacking own country, transfer made...')
            return

        """Check if defending country is a player, and not a black node, if it
        is a player, they will have an associate owned_countries dict which has
        to be adjusted"""
        if defending_player:
            defending_player_owned_countries = defending_player.get_owned_countries()
            defending_player_armies = defending_player_owned_countries[str(move[1])]
        else:
            """If the country isn't owned by anyone, it has 2 armies"""
            defending_player_armies = self.map_graph.get_armies_dict()[str(move[1])]

        """For every army attacking, get outcome of a single attack"""
        for i in range(attacking_player_armies):
            """If there are still defending armies in destination_country"""
            if self.map_graph.get_armies_dict()[str(move[1])] > 0:
                print(str(attacking_player.get_colour()) + ' is attacking ' + str(move[1]))
                defender_chance = random.randint(0, 100) # <= 70 means defender wins
                attacker_chance = random.randint(0, 100) # <= 60 means attacker wins

                """If both players successfully roll, nothing happens"""

                """If defender successfully rolls but attacker doesnt, kill one
                attacking army, defending army stays the same"""
                if defender_chance <= 70 and attacker_chance > 60:
                    print(str(attacking_player.get_colour()) + ' just lost an army in ' + str(move[0]) + ' while attacking')
                    print('it started with: ' + str(attacking_player.get_owned_countries()))

                    new_value = attacking_player.get_owned_countries()[str(move[0])] - 1
                    attacking_player_armies -= 1 #may be able to remove this line entirely
                    attacking_player.add_owned_country(str(move[0]), new_value)
                    self.map_graph.set_army_count(str(move[0]), new_value)
                    print('its total armies is now: ' + str(attacking_player.get_owned_countries()))


                """If attacking army successfully rolls but defender doesnt, kill one
                defending army, attacking army stays the same"""
                if defender_chance > 70 and attacker_chance <= 60:
                    if defending_player:
                        print(str(defending_player.get_colour()) + ' just lost an army in ' + str(move[1]))
                        print('it started with: ' + str(defending_player.get_owned_countries()))

                        new_value = self.map_graph.get_armies_dict()[str(move[1])] - 1

                        defending_player.add_owned_country(move[1], new_value)
                        self.map_graph.set_army_count(str(move[1]), new_value)
                        print('its total armies is now: ' + str(defending_player.get_owned_countries()))

                    else:
                        """No one owns the defending country, so just remove one army in the map object"""
                        value = self.map_graph.get_armies_dict()[str(move[1])] - 1
                        self.map_graph.set_army_count(str(move[1]), value)

            """Else there are no defending armies anymore, flip country to attacking player and
            add the remaining armies to it"""
            if self.map_graph.get_armies_dict()[str(move[1])] == 0:
                attacking_player.add_owned_country(move[1], attacking_player_armies)
                self.map_graph.set_army_count(str(move[1]), attacking_player_armies)
                self.map_graph.change_colour(str(move[1]), str(attacking_player.get_colour()))
                print(str(attacking_player.get_colour()) + ' has invaded ' + str(move[1]))

                """If destination_country is owned by the opposing player"""
                if defending_player:
                    print(str(defending_player.get_colour()) + ' just lost ' + str(move[1]))
                    defending_player.remove_owned_country(move[1])
                else:
                    print(str(move[1]) + ' was not yet owned by anyone')

            if defending_player_armies < 0:
                print('Army count has gone below 0...')

        """Adjust the game map to reflect the new game state after the move"""
        self.adjust_map(self.player1.get_owned_countries(), self.player2.get_owned_countries())

        return

    def total_armies_to_allocate(self, player):
        """Works out how many armies a player has to allocate in this turn. This
        includes playing reinforcements cards, or owning entire regions. Each turn
        automatically gives the players 5 resources."""
        total_armies = 5
        reinf_cards_played = player.consider_reinf_card(self.map_graph)
        if player == self.player1:
            self.player1_reinf_cards_played.append(reinf_cards_played)
        if player == self.player2:
            self.player2_reinf_cards_played.append(reinf_cards_played)

        player.set_reinf_card_count(player.get_reinf_card_count() - reinf_cards_played)
        total_armies += reinf_cards_played * 4

        region_dict = self.map_graph.regions_dict
        countries_owned_by_player = player.get_owned_countries()

        """Check if player owns any entire regions, allocate extra armies if they do"""
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
        #for country in player1_owned_countries.keys():
        for country, value in player1_owned_countries.items():
            self.map_graph.change_colour(str(country), 'b')
            self.map_graph.set_army_count(str(country), player1_owned_countries[str(country)])

        #for country in player2_owned_countries.keys():
        for country, value in player2_owned_countries.items():
            self.map_graph.change_colour(str(country), 'r')
            self.map_graph.set_army_count(str(country), player2_owned_countries[str(country)])

    def allocate_armies(self, player1_additional_armies, player2_additional_armies):
        """Allows both players to use their allocate_armies() function to allocate
        their armies in owned countries"""
        self.player1.allocate_armies(player1_additional_armies)
        self.player2.allocate_armies(player2_additional_armies)

    def perform_moves_in_order(self):
        """Takes an array of moves, and performs them in alternating order. Effectively performing 1 turn"""

        """Calculate how many new armies each player gets this turn"""
        player1_additional_armies = self.total_armies_to_allocate(self.player1)
        player2_additional_armies = self.total_armies_to_allocate(self.player2)

        """Allow both players to allocate their new armies"""
        self.allocate_armies(player1_additional_armies, player2_additional_armies)

        """Adjust the Game object's map to reflect the countries and army counts of the players"""
        self.adjust_map(self.player1.get_owned_countries(), self.player2.get_owned_countries())

        """Get list of moves to make for each player"""
        player1_moves, player2_moves = self.get_moves()

        """Perform the moves in order (currently start with player1)"""
        # TODO: we may need to balance which player's move gets made first

        count = 0
        player1_moves_made_count = 0
        player2_moves_made_count = 0

        """While both players still have moves to make"""
        while len(player1_moves) != 0 or len(player2_moves) != 0:
            count += 1

            """If it is player1's turn to make a move"""
            if count % 2 == 0 and len(player1_moves) > player1_moves_made_count:
                self.make_move(player1_moves[player1_moves_made_count], 'b')
                player1_moves_made_count += 1

            """If it is player2's turn to make a move"""
            if count % 2 == 1 and len(player2_moves) > player2_moves_made_count:
                self.make_move(player2_moves[player2_moves_made_count], 'r')
                player2_moves_made_count += 1

            if len(player2_moves) <= player2_moves_made_count and len(player2_moves) <= player2_moves_made_count:
                """All moves have been made..."""
                break

        """Add any new reinforcement cards earned from this turn to the players"""
        self.player1.set_reinf_card_count(self.player1.check_for_new_reinf_card())
        self.player1.set_reinf_card_count(self.player2.check_for_new_reinf_card())

        """adjust statistic for both players"""
        self.player1_armies.append(self.player1_armies[len(self.player1_armies) - 1] + player1_additional_armies)
        self.player2_armies.append(self.player2_armies[len(self.player2_armies) - 1] + player2_additional_armies)
        self.turn_count += 1

        """Adjust the Game object's map to reflect the countries and army counts of the players"""
        self.adjust_map(self.player1.get_owned_countries(), self.player2.get_owned_countries())

        return
