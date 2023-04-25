import math
import tsplib95
import numpy as np
import tspsolve



class Graph(object):
    def __init__(self, cost_matrix: list, dim: int):
        """
        :param cost_matrix:
        :param dim: dim of the cost matrix
        """
        self.matrix = cost_matrix
        self.rank = dim
        # noinspection PyUnusedLocal
        self.pheromone = [[1 / (dim * dim) for j in range(dim)] for i in range(dim)]


# Class representing the environment of the ant colony
"""
    rho: pheromone evaporation rate
    self: represents the instance of class Environment
    pass: placeholder for future implementation
"""

class Environment:
    def __init__(self, rho):
        self.rho = rho

        # Initialize the environment topology
        self.topology = tsplib95.load('att48-specs/att48.tsp')
        self.dim = self.topology.dimension
        self.coordinates = list(self.topology.node_coords.values())

        # Initialize the pheromone map in the environment
        self.pheromone = []

    def initialize_pheromone_map(self, ant_count):
        value = ant_count / self._Cnn()
        self.pheromone = [[value] * self.dim for _ in range(self.dim)]
        print(f'Initial pheromone value: {value}')

    # Update the pheromone trails in the environment
    def update_pheromone_map(self, ants: list):

        # Evaporate pheromones
        for i, row in enumerate(self.pheromone):
            for j, col in enumerate(row):
                self.pheromone[i][j] *= (1-self.rho)

        # Add new pheromone
        for ant in ants:
            for x in range(len(ant.path)):
                delta_tau = 1 / ant.travelled_distance
                i, j = ant.path[x-1] - 1, ant.path[x] - 1    # -1 each because city values start from 1
                self.pheromone[i][j] += delta_tau
                self.pheromone[j][i] += delta_tau

    # Get the pheromone trails in the environment
    def get_pheromone_map(self):
        return self.pheromone

    def get_distance(self, i, j):
        return self.topology.get_weight(i, j)

    # Get the environment topology
    def get_possible_locations(self):
        return list(self.topology.get_nodes())

    def _Cnn(self):
        cost_matrix = np.array([[self.get_distance(i, j) for i in range(1, self.dim + 1)] for j in range(1, self.dim + 1)])
        path = tspsolve.nearest_neighbor(cost_matrix)

        return sum([cost_matrix[path[i - 1], path[i]] for i in range(self.dim)])

if __name__ == '__main__':
    environment = Environment(0.1)