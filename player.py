import numpy as np


class Player:
    def __init__(self, graph, n_opponents):
        self.graph = graph
        self.positions = np.zeros(n_opponents, dtype=int)

    def play(self):
        return self.graph[self.positions, 0]

    def update_state(self, opponent_moves):
        # opponent_moves: array of 1 and 2
        self.positions = self.graph[self.positions, opponent_moves]
