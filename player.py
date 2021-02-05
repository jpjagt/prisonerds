class Player:
    def __init__(self, graph, n_opponents):
        self.graph = graph
        self.positions = np.zeros(n_opponents, dtype=int)

    def play(self):
        return graph[self.positions, 0]

    def update_state(self, opponent_moves):
        # om: array of 1 and 2
        self.positions = graph[self.positions, opponent_moves]
