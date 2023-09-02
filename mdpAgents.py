# mdpAgents.py
# parsons/20-nov-2017
#
# Version 1
#
# The starting point for CW2.
#
# Intended to work with the PacMan AI projects from:
#
# http://ai.berkeley.edu/
#
# These use a simple API that allow us to control Pacman's interaction with
# the environment adding a layer on top of the AI Berkeley code.
#
# As required by the licensing agreement for the PacMan AI we have:
#
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

# The agent here is was written by Simon Parsons, based on the code in
# pacmanAgents.py

from pacman import Directions
from game import Agent
import api
import random
import game
import util


class MDPAgent(Agent):

    def __init__(self):
        print "Starting up MDPAgent!"
        name = "Pacman"

        # Length and width
        self.x_len = 0
        self.y_len = 0
        self.wall_loc = []

        # policy reward and utility arrays
        self.policy_arr = []
        self.reward_arr = []
        self.utility_arr = []
        self.disc_val = 1

    def getAction(self, state):
        # Set wall locations which determine the Length and width
        self.x_len = self.update_xy_len(api.walls(state))[0]
        self.y_len = self.update_xy_len(api.walls(state))[1]
        self.wall_loc = api.walls(state)

        # return the locations that are not in walls
        all_locations = [(x, y) for x in range(self.x_len) for y in range(self.y_len)]
        self.available_locs = [i for i in all_locations if i not in self.wall_loc]

        # Initialize the initial value of the algorithm
        self.utility_arr = self.init_array(self.x_len, self.y_len)
        self.policy_arr = self.init_array(self.x_len, self.y_len)

        # Set the location infomation
        pacman_loc = api.whereAmI(state)
        capsule_loc = api.capsules(state)
        food_loc = api.food(state)
        ghosts_state_time = api.ghostStatesWithTimes(state)

        # Update each reward of the current game based on ghost, food and capsule locations
        self.reward_arr = self.update_map(ghosts_state_time, food_loc, capsule_loc)

        # perform value iteration and select optimal policy from legal directions
        self.valueIteration()

        # get the actions and remove "STOP" if that is one of them.
        legal = api.legalActions(state)
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)

        # maximize the the utility after selecting the policy
        policy = self.getPolicy(pacman_loc, legal)
        # print policy

        return api.makeMove(policy, legal)

    # BFS: Breadth First Search, to calculate the shortest distance between two points
    def bfs(self, g_loc, available_loc):
        distance = 0
        queue = []
        visited_loc = set()
        x = self.intr(g_loc[0])
        y = self.intr(g_loc[1])
        queue.append((x, y))

        while queue:
            # print queue
            for _ in range(len(queue)):
                cur_x, cur_y = queue.pop(0)
                for nb_x, nb_y in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                    nb_x += cur_x
                    nb_y += cur_y
                    # remove points that we already to visit or they are inaccessible
                    if nb_x < 0 or nb_x >= self.x_len or nb_y < 0 or nb_y >= self.y_len or \
                            (nb_x, nb_y) in self.wall_loc or (nb_x, nb_y) in visited_loc:
                        continue
                    if (nb_x, nb_y) == available_loc:
                        return distance + 1
                    visited_loc.add((nb_x, nb_y))
                    queue.append((nb_x, nb_y))
            distance += 1
        return -1

    # This reward function takes advantage of the information at the current time,
    # and the accumulation of historical values is not involved
    def update_map(self, ghosts_state_time, food_location, capsule_loc):

        # Initialize and specify parameters related to bfs distance
        R_map = self.init_array(self.x_len, self.y_len)
        sub_reward = 0.5
        food_reward = 10

        # Determine food values based on different maps and the amount of food in existence
        for x, y in food_location:
            R_map[x][y] = food_reward
            if len(ghosts_state_time) == 1:
                if len(food_location) > 1:
                    R_map[3][3] = food_reward / 2
                else:
                    R_map[x][y] = food_reward * 2
            else:
                if len(food_location) == 1:
                    R_map[x][y] = food_reward * 10

        for x, y in capsule_loc:
            R_map[x][y] = 10

        # Small map solutions:
        # Set Reward based on Manhattan distance within a smaller range
        """
        Note that here when using Manhattan method, 
        wall obstructions are not taken into account

        we didn't use the BFS (used in medium map) here because after experimentation, 
        we found that it was more minimap-friendly
        """
        if len(ghosts_state_time) == 1:
            for g_loc, ghosts_scared_time in ghosts_state_time:
                # print 'g_loc', g_loc
                ghosts_reward = -8 * self.x_len
                set_distance = 7

                for available_loc in self.available_locs:
                    x = self.intr(g_loc[0])
                    y = self.intr(g_loc[1])
                    R_map[x][y] = ghosts_reward
                    if 0 < self.manhattan(g_loc, available_loc) < set_distance:
                        distance = self.bfs(g_loc, available_loc)
                        x_ind = available_loc[0]
                        y_ind = available_loc[1]
                        ghost_effect_val = self.intr(ghosts_reward * sub_reward ** distance)
                        R_map[x_ind][y_ind] = self.intr(R_map[x_ind][y_ind]) + ghost_effect_val

        # Medium map solutions:
        if len(ghosts_state_time) == 2:
            for g_loc, ghosts_scared_time in ghosts_state_time:
                # print 'g_loc', g_loc
                set_distance = 8 if ghosts_scared_time < 5 else 8
                ghosts_reward = -240 if ghosts_scared_time < 5 else 80
                # Set Reward based on BFS distance within a greater range
                for available_loc in self.available_locs:
                    x = self.intr(g_loc[0])
                    y = self.intr(g_loc[1])
                    R_map[x][y] = ghosts_reward
                    if self.bfs(g_loc, available_loc) < set_distance:
                        distance = self.bfs(g_loc, available_loc)
                        x_ind = available_loc[0]
                        y_ind = available_loc[1]
                        ghost_effect_val = ghosts_reward * sub_reward ** distance
                        R_map[x_ind][y_ind] = R_map[x_ind][y_ind] + ghost_effect_val

        # Where there is a wall, it will be reset to 0
        for x, y in self.wall_loc:
            R_map[x][y] = 0

        # Check the map values if you want,
        # noted that we use the indexes in Python (the initial index is 0)
        # print 'R_map'
        # for i in R_map:
        #     print i
        return R_map

    # Returns the action of maximum utility from the available direction
    def getPolicy(self, pacman_loc, legal):
        move = None
        init_val = -1000000
        for i in legal:
            s = self.get_diction_cord(pacman_loc, i)
            if self.utility_arr[s[0]][s[1]] > init_val:
                move = i
                init_val = self.utility_arr[s[0]][s[1]]
        return move

    # do the value iteration
    def valueIteration(self):
        count = 0
        while count < self.x_len:
            u = self.utility_arr
            for (x, y) in self.available_locs:
                Us = []
                for i in self.can_move([x, y]):
                    st = self.state_trans([x, y], i)
                    Us.append(sum([u[i['x']][i['y']] * i['p'] for i in st]))
                self.utility_arr[x][y] = self.reward_arr[x][y] + self.disc_val * max(Us)

            count = count + 1

    # A state-transition function
    def state_trans(self, location, direction):
        x = location[0]
        y = location[1]

        nb_loc = {'West': {'x': x - 1, 'y': y},
             'East': {'x': x + 1, 'y': y},
             'South': {'x': x, 'y': y - 1},
             'North': {'x': x, 'y': y + 1}}

        moves = ['North', 'East', 'South', 'West']

        r_direction = moves.index(direction) + 1
        if r_direction > len(moves) - 1:
            r_direction = 0

        left = moves[moves.index(direction) - 1]
        right = moves[r_direction]

        adj = [left, right]
        [adj.remove(v) for v in adj if (nb_loc[v]['x'], nb_loc[v]['y'] in self.wall_loc)]

        move_info = [{
            'dir': direction,
            'p': 1.0 - (0.1 * len(adj)),
            'x': nb_loc[direction]['x'],
            'y': nb_loc[direction]['y']}]

        for k in adj: move_info.append({
            'dir': k,
            'p': 0.1,
            'x': nb_loc[k]['x'],
            'y': nb_loc[k]['y']})

        return move_info

    # Translate a direction to a coordinate
    def get_diction_cord(self, pacman, direction):
        x = pacman[0]
        y = pacman[1]
        directions = self.nb_loc(x, y)
        move = None
        for i in directions:
            # print('i',i)
            if i['move'] == direction:
                move = i

        return [move['x'], move['y']]

    # if neightbors are not wall, then can move
    def can_move(self, location):
        x = location[0]
        y = location[1]
        nb_loc = self.nb_loc(x,y)
        return [i['move'] for i in nb_loc if (i['x'], i['y']) not in self.wall_loc]


    # helper functions
    def init_array(self, x_len, y_len):
        return [[0] * y_len for _ in range(x_len)]

    def nb_loc(self,x,y):
        return [{'x': x - 1, 'y': y, 'move': 'West'},
                  {'x': x + 1, 'y': y, 'move': 'East'},
                  {'x': x, 'y': y - 1, 'move': 'South'},
                  {'x': x, 'y': y + 1, 'move': 'North'}]

    def update_xy_len(self, walls):
        self.x_len = max([i[0] for i in walls]) + 1
        self.y_len = max([i[1] for i in walls]) + 1
        return self.x_len, self.y_len

    def manhattan(self, loc1, loc2):
        return abs(loc1[0] - loc2[0]) + abs(loc1[1] - loc2[1])

    def intr(self, value):
        return int(round(value))
