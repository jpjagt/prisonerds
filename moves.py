import numpy as np


class Moves:
    def __init__(self, data):
        self.n = len(data)
        # self.data = N x (N - 1)
        self.data = np.stack(data)

    def player_moves(self, i):
        return self.data[i, :]

    def opponent_moves(self, i, exclude_self=True):
        "get moves of all opponents against player i"
        if not exclude_self:
            return self.data[:, i]
        mask = np.ones(self.n, dtype=bool)
        mask[i] = False
        player_indices = np.full(self.n - 1, i, dtype=int)
        player_indices[:i] -= 1
        return self.data[mask, player_indices]
