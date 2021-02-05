import numpy as np

from player import Player
from graph import Graph
from moves import Moves


class Game:
    def __init__(self, n_graphs):
        self.graphs = np.array([Graph() for _ in range(n_graphs)])
        self.n_graphs = n_graphs
        self.min_rounds = 10
        self.max_rounds = 100
        self.n_graphs_to_keep = int(0.1 * n_graphs)

    def score_moves(self, moves):
        # moves[i, :] should be compared with
        # moves[all_except_i, i]
        scores = np.full(moves.data.shape, -20)
        for i in range(moves.n):
            player_moves = moves.player_moves(i)
            op_moves = moves.opponent_moves(i)
            my_c = player_moves == 1
            op_c = op_moves == 1
            scores[i, my_c & op_c] = -10
            scores[i, my_c & ~op_c] = -25
            scores[i, ~my_c & op_c] = 0
        return scores

    def play_round(self, players):
        # moves: Nx(N-1) array
        # where moves[i, j] is action of player i for player j
        moves = Moves([p.play() for p in players])
        for i, player in enumerate(players):
            player.update_state(moves.opponent_moves(i))
        scores = self.score_moves(moves)
        return scores

    def play_epoch(self):
        n_opponents = self.n_graphs - 1
        n_rounds = np.random.randint(
            self.min_rounds, self.max_rounds, size=(self.n_graphs, n_opponents)
        )
        players = [Player(graph, n_opponents) for graph in self.graphs]
        total_scores = np.zeros(shape=(self.n_graphs, n_opponents))
        for r in range(np.max(n_rounds)):
            round_scores = self.play_round(players)

            # don't update scores for games that have already ended
            round_scores[n_rounds < r] = 0
            total_scores += round_scores
        return total_scores

    def __generate_offspring(self, graph, n_offspring):
        return np.array([graph.clone(mutate=True) for _ in range(n_offspring)])

    def evolve_graphs(self, total_scores):
        sum_of_scores = total_scores.sum(1)
        ranking = np.argsort(sum_of_scores)
        graphs_to_keep = ranking[: self.n_graphs_to_keep]
        parents = self.graphs[graphs_to_keep]

        n_offspring = self.n_graphs // len(parents)
        offspring = np.concatenate(
            [
                self.__generate_offspring(parent, n_offspring)
                for parent in parents
            ]
        )
        np.random.shuffle(offspring)
        self.graphs = offspring[: self.n_graphs]

    def play(self):
        try:
            print("playing until ∞ ... [C-c C-c to interrupt]")
            epoch = 0
            while True:
                total_scores = self.play_epoch()
                print(f"epoch {epoch} ended. stats:")
                print(f"- sum of scores: {total_scores.sum()}")
                print(f"- avg of scores: {total_scores.mean()}")
                print(f"- var of scores: {total_scores.var()}")
                print(f"- max of scores: {total_scores.max()}")
                print(f"- min of scores: {total_scores.min()}")
                print()
                epoch += 1
                self.evolve_graphs(total_scores)
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    game = Game(20)
    game.play()
