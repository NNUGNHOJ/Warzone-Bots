#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  1 17:45:44 2021

@author: katertsif
"""

from copy import deepcopy 
import random
import math 
import game 
import numpy as np 


class MCTS_agent:

    def __init__(self, colour):
        self.colour = colour 
        self.max_iterations_moves = 10000
        self.max_iterations_allocate=5
    
    def choose_moves(self, map, colour, owned_countries, reinf_card_count):
        map_copy = deepcopy(map)
       
        current_owned_countries=deepcopy(owned_countries)
        
        
        """if the agent has any reinforcement cards to play, play them all"""
        if reinf_card_count > 0:
            reinf_cards_played = reinf_card_count
        else:
            reinf_cards_played = 0
        
        chosen_actions=[]
        i=0
        for country in list(current_owned_countries.keys()):
#             i=0
   
           for i in range(3):
                actions = self.get_possible_moves(current_owned_countries, map_copy,country,chosen_actions)


                n_actions = len(actions)

                if len(actions)>0:
                    root = TreeNode(self.colour,actions, n_actions)
                    root.selection(self.max_iterations_moves, current_owned_countries, map_copy) 
                    best_action = root.most_visited_action()
                    current_owned_countries=self.remove_used_armies_from_pool(current_owned_countries,best_action)
                    chosen_actions.append(best_action)
        print('Final chosen actions are:',chosen_actions)
        return chosen_actions,reinf_cards_played,owned_countries

    
    def consider_reinf_card(self, reinf_card_count):
        return reinf_card_count
    
    def get_possible_moves(self,owned_countries,map,country,chosen_actions):
        
        current_neighbours = [n for n in map.map_graph.neighbors(country)]
        for chosen in chosen_actions:
            for neighbour in current_neighbours:
                if chosen[1]==neighbour:
                    current_neighbours.remove(neighbour)
        current_armies_count=owned_countries[str(country)]
        possible_moves=[]
        for neighbour in current_neighbours:
                for i in range(int(current_armies_count + 1)):
                    possible_moves.append((str(country), str(neighbour), i))
                    
        return possible_moves
        
    def allocate_armies(self, additional_armies, owned_countries, map):
        """Takes in a number of armies to be allocated, works out which countries most
         need additional armies. Then allocates armies based on a probability distribution,
         where countries that need armies are more likely to get given them. Then returns
         the owned_countries dict"""

        current_owned_countries = owned_countries
        neighbouring_countries = []
        placement_probability_dict = owned_countries

        """set initial probabilities to 0"""
        placement_probability_dict = dict.fromkeys(placement_probability_dict, 0)

        """For each country, work out how many armies to give it"""
        for country in list(current_owned_countries.keys()):
            neighbouring_countries.append([n for n in map.map_graph.neighbors(country)])

            print('COUNTRY: ' + str(country) + ', has neighbours: ' + str(neighbouring_countries))

            """check if any neighbouring countries have opponent armies"""
            for neighbouring_country in neighbouring_countries[0]:
                """If neighbour colour not the same as player colour"""
                if map.get_colours_dict()[str(neighbouring_country)] != str(self.colour):
                    """If neighbouring country isn't owned by anyone, just add 1"""
                    if map.get_colours_dict()[str(neighbouring_country)] == 'b':
                        placement_probability_dict[str(country)] += 2
                    else:
                        """If country already has an overwhelming number of armies, dont bother adding more, save 
                        them for some other country"""
                        if (map.get_armies_dict()[str(neighbouring_country)] * 1.5) <= map.get_armies_dict()[str(country)]:
                            placement_probability_dict[str(country)] += 1
                        else:
                            """Add probability based on how many armies are in that neighbouring country"""
                            placement_probability_dict[str(country)] += 4
            neighbouring_countries = []

        """Allocate the armies based on the collected probability distribution"""

        """Turn values into probabilities of allocating"""
        total = 0
        list_of_candidates = [*placement_probability_dict]
        probability_distribution = []

        for key, item in placement_probability_dict.items():
            total += item

        for key, item in placement_probability_dict.items():
            placement_probability_dict[str(key)] = item / total
            probability_distribution.append(item / total)

        """Choose countries 'randomly' but weighted based on probability distribution"""
        chosen_countries = random.choices(population=list_of_candidates,
                                          weights=probability_distribution,
                                          k=additional_armies)

        """Allocate the chosen countries"""
        for country in chosen_countries:
            owned_countries[str(country)] += 1

        return owned_countries

    
    def get_possible_allocate_armies(self,additional_armies,owned_countries):
        possible_moves=[]
        for country in list(owned_countries.keys()):
            for i in range(additional_armies):
                possible_moves.append((country,i))
        return possible_moves
    
    def remove_used_armies_from_pool(self, current_owned_countries, move):
        """Removes armies from a country based on a move having been selected.
        e.g. the move is (Iceland, Britain, 3) means removing 3 armies from Iceland.
        This is not done to the actual game, but just as a temporary counter to keep
        track of how many armies are left to play with in this particular turn"""
        country_to_be_altered = move[0]
        armies_to_deduct = move[2]
        current_owned_countries[str(country_to_be_altered)] -= armies_to_deduct
        return current_owned_countries

class TreeNode:
    
    def __init__(self,colour, actions, n_actions, parent = None,childIdx=-1): 
        self.colour=colour
        self.parent = parent 
#         self.state=state
#         self.map=map
        self.n_actions = n_actions
        self.actions = actions 
        self.children = [None for i in range(self.n_actions)]
        self.rollout_depth = 30
        self.childIdx=childIdx
        self.K = math.sqrt(2)
        self.epsilon = 1e-6
        if self.parent != None:
            self.n_depth = parent.n_depth + 1
        else:
            self.n_depth=0
        self.lower_bound = np.inf
        self.upper_bound = - np.inf
        self.n_visits = 0.0
        self.totalValue = 0.0
        
    
    def selection(self, max_iterations, current_state, map_copy):
        for i in range(max_iterations):
            state = deepcopy(current_state)
            map = deepcopy(map_copy)
            selected, state, map = self.TreePolicy(state, map)
            delta, state, map = selected.rollout(state, map, current_state) 
          
            selected.backpropagate(delta)
            
    def TreePolicy(self, state, map): 
        current = self 
        while ( not game.Game('Heuristic','MCTS').check_game_over() and current.n_depth < self.rollout_depth) :
            if current.not_fully_expanded():
                
                current, state, map = current.expand(state, map)
                return current, state, map
            else: 
               
                next, state, map = current.UCT(state, map)
                current = next
        return current, state, map
    
    def expand(self, state, map):
        best_action = 0 
        best_value = -1 
        
        
        for i in range(len(self.children)):
            x = np.random.rand(1)
            if x > best_value and self.children[i] == None : 
                best_action = i
                best_value = x
      
        state, map = self.make_move(best_action, state, map)
        state = self.remove_used_armies_from_pool(best_action, state, map)

        
        tn=TreeNode(colour=self.colour,childIdx=best_action,n_actions=self.n_actions, actions=self.actions)
        self.children[best_action]=TreeNode(colour=self.colour,childIdx=best_action,n_actions=self.n_actions, actions=self.actions,parent=self)
        return tn, state, map
    
    def UCT(self, state, map):
        selected = None
        best_value = - np.inf
        for child in self.children:
            hv_val = child.totalValue
        
            childValue = hv_val / (child.n_visits + self.epsilon)
            childValue = child.normalise(childValue, self.lower_bound, self.upper_bound)
            UCT = childValue + self.K * math.sqrt(np.log(self.n_visits+1) / (child.n_visits + self.epsilon))
            UCT= (UCT + self.epsilon) *(1.0 +self.epsilon *(random.random()-0.5))
            
            
            if UCT > best_value: 
                selected = child 
                best_value = UCT 
            
        if selected == None: 
            print("Error in UCT")
        state, map = self.make_move(selected.childIdx, state, map)
        state = self.remove_used_armies_from_pool(selected.childIdx, state, map)
        return selected, state, map
    
    def rollout(self, state, map, current_state):
        depth = self.n_depth

         
        while (not self.finish_rollout(depth)) and self.n_actions>1:
            action = random.randint(0,self.n_actions-1)
           
            state, map = self.make_move(action, state, map)
            state = self.remove_used_armies_from_pool(action, state, map)
            

            depth += 1 
        delta = self.valueState(state, map, current_state)
        if delta < self.upper_bound: 
            self.upper_bound = delta 
        if delta < self.lower_bound: 
            self.lower_bound = delta
        return delta, state, map
    
    
        

    def valueState(self, state, map, current_state): 
        gameOver = game.Game('Heuristic','MCTS').check_game_over()
        winner = False 
        loser = False 
        score = 0 
        
        if len(state) == map.map_graph.number_of_nodes():
            winner = True 
        if len(state) == 0:
            loser = True 
        if len(state) > len(current_state):
            score += 20 
        elif len(state) == len(current_state):
            score += 5 
        else: 
            score += -20 

        if gameOver and winner: 
            score += 1000 
        if gameOver and loser:
            score += -1000
        if 'Alaska' in state and 'Northwest territory' in state and \
            'Greenland' in state and 'Alberta' in state and 'Ontario' in state and \
            'Quebec' in state and 'Western United States' in state and \
            'Eastern United States'in state and 'Mexico' in state:
            score += 500
        if 'Venezuela' in state and 'Brazil' in state and \
            'Peru' in state and 'Argentina' in state:
            score += 500
        if 'North Africa' in state and 'Egypt' in state and \
            'East Africa' in state and 'Congo' in state and 'South Africa' in state and \
            'Madagascar' in state:
            score += 500
        if 'Iceland' in state and 'Scandinavia' in state and \
            'Great Britain' in state and 'Northern Europe' in state and 'Western Europe' in state and \
            'Southern Europe' in state and 'Ukraine' in state:
            score += 500
        if 'Ural' in state and 'Siberia' in state and \
            'Yakutsk' in state and 'Kamchatka' in state and 'Japan' in state and \
            'Mongolia' in state and 'Irkutsk' in state and \
            'China'in state and 'Siam' in state and 'India' in state and \
            'Middle East' in state and 'Kazakhstan' in state:
            score += 500
        if 'Indonesia' in state and 'New Guinea' in state and \
            'Eastern Australia' in state and 'Western Australia' in state:
            score += 500
        return score
    
    def finish_rollout(self, depth):
        if depth >= self.rollout_depth: 
            return True 
        elif game.Game('Heuristic','MCTS').check_game_over():
            return True 
        else:
            return False 
    
    def backpropagate(self, result):
        while self != None: 
            self.n_visits += 1 
            self.totalValue += result 
            
            if result < self.upper_bound: 
                self.upper_bound = result 
            if result > self.lower_bound: 
                self.lower_bound = result
            if self.parent == None:
                break
            self= self.parent
    
    def most_visited_action(self):
        selected = -1 
        best_value = - np.inf
        all_equal = True 
        first = -1 
        for i in range(len(self.children)):
            if self.children[i] != None: 
                if first == -1:
                    first = self.children[i].n_visits
                elif(first != self.children[i].n_visits):
                    all_equal = False 
                childValue = self.children[i].n_visits
                childValue= (childValue + self.epsilon) *(1.0 +self.epsilon *(random.random()-0.5))
                if childValue > best_value: 
                    best_value = childValue
                    selected = i 
        selected_action=self.actions[self.children[selected].childIdx]
        if selected == -1:
            print("Error in most visited action")
        if all_equal == True: 
            selected_action = self.bestAction()   
       
        return selected_action 

    def bestAction(self):
        selected = -1
        best_value = -np.inf
        for i in range(len(self.children)):
            if self.children[i] != None: 
                childValue = self.children[i].totalValue / (self.children[i].n_visits + self.epsilon) 
                childValue= (childValue + self.epsilon) *(1.0 +self.epsilon *(random.random()-0.5))
                
                if childValue > best_value: 
                    best_value = childValue
                    selected = i 
        selected_action=self.actions[self.children[selected].childIdx]
        return selected_action
    
    def not_fully_expanded(self):
        for child in self.children:
            if child == None: 
                return True 
        return False 
            
    def normalise(self, childValue, min, max): 
        if min < max: 
            return (childValue - min) / (max - min)
        else: 
            return childValue 
        
        
        
    def make_move(self, action, state, map):
        """Takes a single move and performs it on the map graph, a move consists
        of (origin_country, destination_country, armies_to_move)"""
            
        if self.colour == 'b':
            attacking_player_colour='b'
            """If destination_country isn't owned by either player"""
            if map.get_colours_dict()[self.actions[action][1]] == 'k':
                defending_player_colour = 'k'
            elif map.get_colours_dict()[self.actions[action][1]]=='b':
                defending_player_colour = None
            else:
                defending_player_colour='r'
        else:
            attacking_player_colour = 'r'
            """destination_country isn't owned by either player"""
            if map.get_colours_dict()[self.actions[action][1]] == 'k':
                defending_player_colour = 'k'
            elif map.get_colours_dict()[self.actions[action][1]]=='r':
                defending_player_colour = None
            else:
                defending_player_colour = 'b'
        """Check that the player still owns the origin_country, if it does not, 
        then return without making the move."""
        if map.get_colours_dict()[self.actions[action][0]] != str(self.colour):
            return state, map

        """Check if the origin country still has all the armies the move wants to
        utilise"""

        """If the origin_country does not have as many armies as the move
        requires, then just use however many armies there are left."""
        if map.get_armies_dict()[self.actions[action][1]] >= self.actions[action][2]:
            attacking_player_armies = self.actions[action][2]
        else:
            attacking_player_armies = map.get_armies_dict()[self.actions[action][0]]

        """If the same player owns both countries, just transfer the armies"""
        if map.get_colours_dict()[self.actions[action][0]] == map.get_colours_dict()[self.actions[action][1]]:
            origin_army_count = map.get_armies_dict()[self.actions[action][0]]
            destination_army_count = map.get_armies_dict()[self.actions[action][1]]

            map.set_army_count(self.actions[action][0], (origin_army_count - attacking_player_armies))
            map.set_army_count(self.actions[action][1], (destination_army_count + attacking_player_armies))
            state.update({self.actions[action][1]:destination_army_count + attacking_player_armies})
            state[self.actions[action][0]] = origin_army_count - attacking_player_armies
            return state, map

        """Check if defending country is a player, and not a black node, if it
        is a player, they will have an associate owned_countries dict which has
        to be adjusted"""
        if defending_player_colour=='r':
            
            defending_player_owned_countries ={}
            armies= map.get_armies_dict()
            countries_colour= map.get_colours_dict()
            for i in range(len(countries_colour)):
                key=list(countries_colour.keys())[i]
                if countries_colour[key]=='r':
                    defending_player_owned_countries.update({key:armies[key]})
                    
            defending_player_armies = defending_player_owned_countries[self.actions[action][1]]
        elif defending_player_colour=='b':
            defending_player_owned_countries ={}
            armies = map.get_armies_dict()
            countries_colour= map.get_colours_dict()
            for i in range(len(countries_colour)):
                key=list(countries_colour.keys())[i]
                if countries_colour[key]=='b':
                    defending_player_owned_countries.update({key:armies[key]})
            defending_player_armies = defending_player_owned_countries[self.actions[action][1]]
        else:
            """If the country isn't owned by anyone, it has 2 armies"""
            defending_player_armies = map.get_armies_dict()[self.actions[action][1]]

        """For every army attacking, get outcome of a single attack"""
        for i in range(int(attacking_player_armies)):
            """If there are still defending armies in destination_country"""
            if map.get_armies_dict()[self.actions[action][1]] > 0:
                
                defender_chance = random.randint(0, 100) # <= 70 means defender wins
                attacker_chance = random.randint(0, 100) # <= 60 means attacker wins

                """If both players successfully roll, nothing happens"""

                """If defender successfully rolls but attacker doesnt, kill one
                attacking army, defending army stays the same"""
                if defender_chance <= 70 and attacker_chance > 60:
                    

                    new_value = state[self.actions[action][0]] - 1
                    attacking_player_armies -= 1 #may be able to remove this line entirely
                    state[self.actions[action][0]] = new_value
                    map.set_army_count(self.actions[action][0], new_value)
                   


                """If attacking army successfully rolls but defender doesnt, kill one
                defending army, attacking army stays the same"""
                if defender_chance > 70 and attacker_chance <= 60:
                    if defending_player_colour=='r' or defending_player_colour=='b':
                        

                        new_value = map.get_armies_dict()[self.actions[action][1]] - 1
                        
                        defending_player_owned_countries.update({self.actions[action][1]:new_value})
                        
                        map.set_army_count(self.actions[action][1], new_value)
                        

                    else:
                        """No one owns the defending country, so just remove one army in the map object"""
                        value = map.get_armies_dict()[self.actions[action][1]] - 1
                        map.set_army_count(self.actions[action][1], value)

            """Else there are no defending armies anymore, flip country to attacking player and
            add the remaining armies to it"""
            if map.get_armies_dict()[self.actions[action][1]] == 0:
                state.update({self.actions[action][1]:attacking_player_armies})
                
                map.set_army_count(self.actions[action][1], attacking_player_armies)
                map.change_colour(self.actions[action][1], self.colour)
               

                """If destination_country is owned by the opposing player"""
                if defending_player_colour=='r' or defending_player_colour=='b':
                    
                    
                    defending_player_owned_countries.pop(self.actions[action][1])
                

            if defending_player_armies < 0:
                print('Army count has gone below 0...')

        """Adjust the game map to reflect the new game state after the move"""
        if defending_player_colour=='r' :
            map = self.adjust_map(state, defending_player_owned_countries, map)
        elif defending_player_colour=='b':
            map = self.adjust_map(defending_player_owned_countries,state, map)
        else:
            map = self.adjust_map(state, {}, map)
        
        return state, map
    
    def adjust_map(self, player1_owned_countries, player2_owned_countries, map):
        """Changes the map to reflect the owned countries and army counts as per the players"""
        #for country in player1_owned_countries.keys():
        for country, value in player1_owned_countries.items():
            map.change_colour(str(country), 'b')
            map.set_army_count(str(country), player1_owned_countries[str(country)])

        #for country in player2_owned_countries.keys():
        for country, value in player2_owned_countries.items():
            map.change_colour(str(country), 'r')
            map.set_army_count(str(country), player2_owned_countries[str(country)])
        return map
    
   
    
    def remove_used_armies_from_pool(self, move, state, map):
        """Removes armies from a country based on a move having been selected.
        e.g. the move is (Iceland, Britain, 3) means removing 3 armies from Iceland.
        This is not done to the actual game, but just as a temporary counter to keep
        track of how many armies are left to play with in this particular turn"""
        country_to_be_altered = self.actions[move][0]
        armies_to_deduct = self.actions[move][2]
        state[str(country_to_be_altered)] -= armies_to_deduct
        return state
