#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  1 17:45:44 2021

@author: katertsif
"""

from copy import deepcopy 
import random
import test_game
import math 
import numpy as np 


class MCTS_agent:

    def __init__(self, colour):
        self.colour = colour 
        self.max_iterations = 3

    def choose_moves(self, map, colour, owned_countries, reinf_card_count):
        map_copy = deepcopy(map)
       
        current_owned_countries=deepcopy(owned_countries)
        
        print('My current countries are: ',current_owned_countries)
        
        """if the agent has any reinforcement cards to play, play them all"""
        if reinf_card_count > 0:
            reinf_cards_played = reinf_card_count
        else:
            reinf_cards_played = 0
        
        chosen_actions=[]
        for country in list(current_owned_countries.keys()):
            
            actions = self.get_possible_moves(current_owned_countries, map_copy,country)
            n_actions = len(actions)
            while current_owned_countries[country]>0:
                actions = self.get_possible_moves(current_owned_countries, map_copy,country)
                n_actions = len(actions)
                if len(actions)>0:
                    root = TreeNode(self.colour,actions, n_actions)

                    root.selection(self.max_iterations, current_owned_countries, map_copy) 
                    action = root.most_visited_action()
                    current_owned_countries=self.remove_used_armies_from_pool(current_owned_countries,action)
                    print('My chosen action is: ',action)
            
                    chosen_actions.append(action)
            
            
         

        
        print('The final chosen actions are:',chosen_actions)
        return chosen_actions,reinf_cards_played,owned_countries

    
    def consider_reinf_card(self, reinf_card_count):
        return reinf_card_count
    
#     def get_possible_moves(self, owned_countries, map):
#         """Returns an array of all the possible moves the agent could make, where
#         a move is (origin_country, destination_country, armies)"""
#         possible_moves = []

#         for country in list(owned_countries.keys()):
#             current_neighbours = [n for n in map.map_graph.neighbors(country)]
#             current_armies_count = owned_countries[str(country)]
#             for neighbour in current_neighbours:
#                 for i in range(current_armies_count + 1):
#                     possible_moves.append((str(country), str(neighbour), i))

#         return possible_moves
    def get_possible_moves(self,owned_countries,map,country):
        
        current_neighbours = [n for n in map.map_graph.neighbors(country)]
        current_armies_count=owned_countries[str(country)]
        possible_moves=[]
        for neighbour in current_neighbours:
                for i in range(current_armies_count + 1):
                    possible_moves.append((str(country), str(neighbour), i))
                    
        return possible_moves
        
    
    def allocate_armies(self, additional_armies, owned_countries):
        print(str(self.colour) + ' owns these countries: ' + str(owned_countries))
        while additional_armies > 0:
            country = random.choice(list(owned_countries.keys()))
            print('Algorithm has chosen ' + str(country) + ' to be allocated an army')
            owned_countries[str(country)] += 1
            additional_armies -= 1

        print('after allocating, ' + str(self.colour) + ' owns these countries: ' + str(owned_countries))

        return owned_countries
    
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
    
    def __init__(self,colour, actions, n_actions, parent = None,childIdx=-1,state=None,map=None): 
        self.colour=colour
        self.parent = parent 
        self.state=state
        self.map=map
        self.n_actions = n_actions
        self.actions = actions 
        self.children = [None for i in range(self.n_actions)]
        self.rollout_depth = 10
        self.childIdx=childIdx
        self.K = math.sqrt(2)
        self.epsilon = 0.5
        if self.parent != None:
            self.n_depth = parent.n_depth + 1
        else:
            self.n_depth=0
        self.lower_bound = - np.inf
        self.upper_bound = np.inf
        self.n_visits = 0.0
        self.totalValue = 0.0
        
    
    def selection(self, max_iterations, state, map):
        for i in range(max_iterations):
           
            self.state = deepcopy(state)
            self.map = deepcopy(map)
            selected = self.TreePolicy()
            delta = selected.rollout()
            print('The childs delta is :',delta)
            selected.backpropagate(delta)
            
    def TreePolicy(self): 
        current = self 
        while ( not test_game.check_game_over() and current.n_depth < self.rollout_depth) :
            if current.not_fully_expanded():
                print('The algorithm is in the expand phase')
                current=current.expand()
                return current
            else: 
                print('The algorithm is in UCT phase')
                next = current.UCT()
                current = next
        return current
    
    def expand(self):
        best_action = 0 
        best_value = -1 
        
        
        for i in range(len(self.children)):
            x = np.random.rand(1)
            if x > best_value and self.children[i] == None : 
                best_action = i
                best_value = x
               
        print("The best action is : ",best_action)
        print('Childrens length is: ',len(self.children) )
        print('The number of actions in total is: ', self.n_actions)
        self.make_move(best_action)
        self.remove_used_armies_from_pool(best_action)
#         self.actions=self.get_possible_moves()
#         self.n_actions=len(self.actions)
        
        tn=TreeNode(colour=self.colour,childIdx=best_action,n_actions=self.n_actions, actions=self.actions,state=self.state,map=self.map)
        self.children[best_action]=TreeNode(colour=self.colour,childIdx=best_action,n_actions=self.n_actions, actions=self.actions,parent=self,state=self.state,map=self.map)
        return tn
    
    def UCT(self):
        selected = None
        best_value = - np.inf
         
        
        for child in self.children:
            print(child)
            
            hv_val = child.totalValue
            childValue = hv_val / (child.n_visits + self.epsilon)
#             childValue = child.normalise(childValue, child.lower_bound, child.upper_bound)
            UCT = childValue + self.K * math.sqrt(np.log(self.n_visits+1) / (child.n_visits + self.epsilon))
            print("The childs UCT is :", UCT)
            print('The best value is :', best_value)
            if UCT > best_value: 
                selected = child 
                best_value = UCT 
            
          

        if selected == None: 
            print("Error in UCT")
        
        self.make_move(selected.childIdx)
        self.remove_used_armies_from_pool(selected.childIdx)
#         self.actions=self.get_possible_moves()
#         self.n_actions=len(self.actions)
        return selected
    
    def rollout(self):
        depth = self.n_depth
#         action = random.randint(0,self.n_actions)
#         i=0
#         while state[self.actions[action][0]]==0 or (state[self.actions[action][0]]-self.actions[action][2])<0:
#             action = random.randint(0,self.n_actions-1)
#             i+=1
#             if i==len(self.actions):
#                 delta=-100
#                 return delta,state,map
         
        while (not self.finish_rollout(depth)) and self.n_actions>1:
            action = random.randint(0,self.n_actions-1)
           
            self.make_move(action)
            self.remove_used_armies_from_pool(action)
            
#             self.actions=self.get_possible_moves()
#             self.n_actions=len(self.actions)
            depth += 1 
        delta = self.valueState()
        if delta < self.upper_bound: 
            self.upper_bound = delta 
        if delta < self.lower_bound: 
            self.lower_bound = delta
        return delta 
    
    
        

    def valueState(self): 
        gameOver = test_game.check_game_over()
        winner = False 
        loser = False 
        
        if len(self.state) == self.map.map_graph.number_of_nodes():
            winner = True 
        if len(self.state) == 0:
            loser = True 
        score = len(self.state)
        if gameOver and winner: 
            score = 1000 
        if gameOver and loser:
            score = -1000
        return score
    
    def finish_rollout(self, depth):
        if depth >= self.rollout_depth: 
            return True 
        elif test_game.check_game_over():
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
        
        
        
    def make_move(self, action):
        """Takes a single move and performs it on the map graph, a move consists
        of (origin_country, destination_country, armies_to_move)"""
            
        if self.colour == 'b':
            attacking_player_colour='b'
            """If destination_country isn't owned by either player"""
            if self.map.get_colours_dict()[self.actions[action][1]] == 'k':
                defending_player_colour = 'k'
            elif self.map.get_colours_dict()[self.actions[action][1]]=='b':
                defending_player_colour = None
            else:
                defending_player_colour='r'
        else:
            attacking_player_colour = 'r'
            """destination_country isn't owned by either player"""
            if self.map.get_colours_dict()[self.actions[action][1]] == 'k':
                defending_player_colour = 'k'
            elif self.map.get_colours_dict()[self.actions[action][1]]=='r':
                defending_player_colour = None
            else:
                defending_player_colour = 'b'
        """Check that the player still owns the origin_country, if it does not, 
        then return without making the move."""
        if self.map.get_colours_dict()[self.actions[action][0]] != str(self.colour):
            return 

        """Check if the origin country still has all the armies the move wants to
        utilise"""

        """If the origin_country does not have as many armies as the move
        requires, then just use however many armies there are left."""
        if self.map.get_armies_dict()[self.actions[action][1]] >= self.actions[action][2]:
            attacking_player_armies = self.actions[action][2]
        else:
            attacking_player_armies = self.map.get_armies_dict()[self.actions[action][0]]

        """If the same player owns both countries, just transfer the armies"""
        if self.map.get_colours_dict()[self.actions[action][0]] == self.map.get_colours_dict()[self.actions[action][1]]:
            origin_army_count = self.map.get_armies_dict()[self.actions[action][0]]
            destination_army_count = self.map.get_armies_dict()[self.actions[action][1]]

            self.map.set_army_count(self.actions[action][0], (origin_army_count - attacking_player_armies))
            self.map.set_army_count(self.actions[action][1], (destination_army_count + attacking_player_armies))
#             attacking_player.add_owned_country(str(move[0]), (origin_army_count - attacking_player_armies))
#             attacking_player.add_owned_country(str(move[1]), (destination_army_count + attacking_player_armies))
            self.state.update({self.actions[action][1]:destination_army_count + attacking_player_armies})
            self.state[self.actions[action][0]] = origin_army_count - attacking_player_armies
            
            return

        """Check if defending country is a player, and not a black node, if it
        is a player, they will have an associate owned_countries dict which has
        to be adjusted"""
        if defending_player_colour=='r':
            defending_player_owned_countries ={}
            armies=self.map.get_armies_dict()
            countries_colour=self.map.get_colours_dict()
            for i in range(len(countries_colour)):
                key=list(countries_colour.keys())[i]
                if countries_colour[key]=='r':
                    defending_player_owned_countries.update({key:armies[key]})
                    
            defending_player_armies = defending_player_owned_countries[self.actions[action][1]]
        elif defending_player_colour=='b':
            defending_player_owned_countries ={}
            armies=self.map.get_armies_dict()
            countries_colour=self.map.get_colours_dict()
            for i in range(len(countries_colour)):
                key=list(countries_colour.keys())[i]
                if countries_colour[key]=='b':
                    defending_player_owned_countries.update({key:armies[key]})
            defending_player_armies = defending_player_owned_countries[self.actions[action][1]]
        else:
            """If the country isn't owned by anyone, it has 2 armies"""
            defending_player_armies = self.map.get_armies_dict()[self.actions[action][1]]

        """For every army attacking, get outcome of a single attack"""
        for i in range(attacking_player_armies):
            """If there are still defending armies in destination_country"""
            if self.map.get_armies_dict()[self.actions[action][1]] > 0:
                
                defender_chance = random.randint(0, 100) # <= 70 means defender wins
                attacker_chance = random.randint(0, 100) # <= 60 means attacker wins

                """If both players successfully roll, nothing happens"""

                """If defender successfully rolls but attacker doesnt, kill one
                attacking army, defending army stays the same"""
                if defender_chance <= 70 and attacker_chance > 60:
                    

                    new_value = self.state[self.actions[action][0]] - 1
                    attacking_player_armies -= 1 #may be able to remove this line entirely
                    self.state[self.actions[action][0]] = new_value
#                     attacking_player.add_owned_country(str(move[0]), new_value)
                    self.map.set_army_count(self.actions[action][0], new_value)
                   


                """If attacking army successfully rolls but defender doesnt, kill one
                defending army, attacking army stays the same"""
                if defender_chance > 70 and attacker_chance <= 60:
                    if defending_player_colour=='r' or defending_player_colour=='b':
                        

                        new_value = self.map.get_armies_dict()[self.actions[action][1]] - 1
                        
                        defending_player_owned_countries.update({self.actions[action][1]:new_value})
                        
                        self.map.set_army_count(self.actions[action][1], new_value)
                        

                    else:
                        """No one owns the defending country, so just remove one army in the map object"""
                        value = self.map.get_armies_dict()[self.actions[action][1]] - 1
                        self.map.set_army_count(self.actions[action][1], value)

            """Else there are no defending armies anymore, flip country to attacking player and
            add the remaining armies to it"""
            if self.map.get_armies_dict()[self.actions[action][1]] == 0:
                self.state.update({self.actions[action][1]:attacking_player_armies})
                
                self.map.set_army_count(self.actions[action][1], attacking_player_armies)
                self.map.change_colour(self.actions[action][1], self.colour)
               

                """If destination_country is owned by the opposing player"""
                if defending_player_colour=='r' or defending_player_colour=='b':
                    
                    
                    defending_player_owned_countries.pop(self.actions[action][1])
                

            if defending_player_armies < 0:
                print('Army count has gone below 0...')

        """Adjust the game map to reflect the new game state after the move"""
        if defending_player_colour=='r' :
            self.adjust_map(self.state,defending_player_owned_countries)
        elif defending_player_colour=='b':
            self.adjust_map(defending_player_owned_countries,self.state)
        else:
            self.adjust_map(self.state,{})
        
        return 
    
    def adjust_map(self, player1_owned_countries, player2_owned_countries):
        """Changes the map to reflect the owned countries and army counts as per the players"""
        #for country in player1_owned_countries.keys():
        for country, value in player1_owned_countries.items():
            self.map.change_colour(str(country), 'b')
            self.map.set_army_count(str(country), player1_owned_countries[str(country)])

        #for country in player2_owned_countries.keys():
        for country, value in player2_owned_countries.items():
            self.map.change_colour(str(country), 'r')
            self.map.set_army_count(str(country), player2_owned_countries[str(country)])
        return 
    
    def get_possible_moves(self):
        """Returns an array of all the possible moves the agent could make, where
        a move is (origin_country, destination_country, armies)"""
        possible_moves = []

        for country in list(self.state.keys()):
            current_neighbours = [n for n in self.map.map_graph.neighbors(country)]
            current_armies_count = self.state[str(country)]
            for neighbour in current_neighbours:
                for i in range(current_armies_count + 1):
                    possible_moves.append((str(country), str(neighbour), i))

        return possible_moves
    
    def remove_used_armies_from_pool(self, move):
        """Removes armies from a country based on a move having been selected.
        e.g. the move is (Iceland, Britain, 3) means removing 3 armies from Iceland.
        This is not done to the actual game, but just as a temporary counter to keep
        track of how many armies are left to play with in this particular turn"""
        country_to_be_altered = self.actions[move][0]
        armies_to_deduct = self.actions[move][2]
        self.state[str(country_to_be_altered)] -= armies_to_deduct
        return 
