# Written by James Morrow. Please direct enquiries to jamesmorrow10@gmail

import numpy as np
import random as random
import copy


class forest:
    """
    The forest class has a 2D (numpy) array of sites. These may be: empty(0), have a tree(1) or be currently  burning(2).
    Trees have a chance to combust with probability combustion_probability. Empty sites may spawn new trees with
    probability genesis_probability.
    The update method advances the forest array forward one unit in time implementing the simple cellular
    automaton forest fire model, see https://en.wikipedia.org/wiki/Forest-fire_model
    Currently, the forest comprises a square lattice of sites with 8 nearest neighbours. 
    """
    def __init__(self, rows, columns, genesis_probability, combustion_probability, seed_value=None):
        self.automaton_array = np.zeros((rows, columns))
        self.combustion_probability = combustion_probability
        self.genesis_probability = genesis_probability
        random.seed(seed_value)

    def neighbour_site_exists(self, neighbour_row, neighbour_column):
        try:
            self.automaton_array[neighbour_row][neighbour_column]
        except IndexError:
            return False
        else:
            # here Python's admittance of negative indices is somewhat unhelpful. Regardless, we can filter them out.
            if neighbour_row < 0 or neighbour_column < 0:
                return False
            else:
                return True

    def update(self):
        """performs one time step of the forest fire model https://en.wikipedia.org/wiki/Forest-fire_model"""
        # looping through forest to either create trees(1) on empty sites(0) or to start fires(2) on trees(1)
        old_automaton_array = copy.deepcopy(self.automaton_array)
        for row in range(0, len(self.automaton_array)):
            for column in range(0, len(self.automaton_array[row])):
                # empty site(0) create new tree(1) with probability of genesis_probability
                if old_automaton_array[row][column] == 0:
                    random_number = random.uniform(0.0, 1.0)
                    if random_number < self.genesis_probability:
                        self.automaton_array[row][column] = 1
                # site with tree(1) may set fire(2) either by self combusting with probability
                # combustion_probability, or because a neighbouring tree is on fire
                elif old_automaton_array[row][column] == 1:
                    random_number = random.uniform(0.0, 1.0)
                    if random_number < self.combustion_probability:
                        self.automaton_array[row][column] = 2
                    for neighbour_row in range(row - 1, row + 2):
                        for neighbour_column in range(column - 1, column + 2):
                            if self.neighbour_site_exists(neighbour_row, neighbour_column):
                                """although this loops through the current point, we already know that the 
                                old_automaton_array is one before we reach here. So there is no problem of reigniting an 
                                old burning site, which is due to burn out."""
                                if old_automaton_array[neighbour_row][neighbour_column] == 2:
                                    self.automaton_array[row][column] = 2
                # burning site(2) burns out to leave an empty site(0)
                elif old_automaton_array[row][column] == 2:
                    self.automaton_array[row][column] = 0

    def __str__(self):
        """
        :return: string representation of the current state of the 2D (numpy) self.automaton_array
        """
        return str(self.automaton_array)