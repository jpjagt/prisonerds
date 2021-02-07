import numpy as np

from player import Player
from graph import Graph
from moves import Moves
import famous_strategies


class Game:
    def __init__(self, n_graphs=None, graphs=None):
        if graphs is None:
            assert n_graphs is not None, "n_graphs or graphs gotta be set bro"
            self.graphs = np.array([Graph() for _ in range(n_graphs)])
        else:
            self.graphs = np.array(graphs)
            n_graphs = len(self.graphs)
        self.n_graphs = n_graphs
        self.min_rounds = 10
        self.max_rounds = 100
        self.n_graphs_to_keep = int(0.1 * n_graphs)

    def score_moves(self, moves, op_moves=None):
        if op_moves is None:
            op_moves = moves
            exclude_self = True
        else:
            exclude_self = False
        scores = np.full(moves.data.shape, -20)
        for i in range(moves.n):
            my_c = moves.player_moves(i) == 1
            op_c = op_moves.opponent_moves(i, exclude_self=exclude_self) == 1
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
        print(set([graph.data.shape[0] for graph in self.graphs]))
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
        return np.array(
            [graph.clone(mutate=True) for _ in range(n_offspring - 1)]
            + [graph.clone(mutate=False)]
        )

    def evolve_graphs(self, total_scores):
        sum_of_scores = total_scores.sum(1)
        ranking = np.argsort(sum_of_scores)[::-1]
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

    def play_two_groups(self, graphs1, graphs2, n_rounds=20):
        players1 = [Player(graph, len(graphs2)) for graph in graphs1]
        players2 = [Player(graph, len(graphs1)) for graph in graphs2]
        total_scores = None
        for r in range(n_rounds):
            moves1 = Moves([p.play() for p in players1])
            moves2 = Moves([p.play() for p in players2])
            for i, player in enumerate(players1):
                player.update_state(
                    moves2.opponent_moves(i, exclude_self=False)
                )
            for i, player in enumerate(players2):
                player.update_state(
                    moves1.opponent_moves(i, exclude_self=False)
                )

            scores = self.score_moves(moves1, moves2)
            if total_scores is None:
                total_scores = scores
            else:
                total_scores += scores
        return total_scores

    def validate(self):
        total_scores = self.play_two_groups(
            self.graphs, famous_strategies.strategies
        )
        print("validation stats:")
        self.log_score_stats(total_scores)

    def log_score_stats(self, scores):
        print(f"- sum of scores: {scores.sum()}")
        print(f"- avg of scores: {scores.mean()}")
        print(f"- var of scores: {scores.var()}")
        print(f"- max of scores: {scores.max()}")
        print(f"- min of scores: {scores.min()}")

    def play(self):
        try:
            print("playing until ∞ ... [C-c C-c to interrupt]")
            epoch = 0
            while True:
                total_scores = self.play_epoch()
                print(f"epoch {epoch} ended.")
                self.validate()
                print()
                epoch += 1
                self.evolve_graphs(total_scores)
        except KeyboardInterrupt:
            pass


def main(init_with_strats=False):
    if not init_with_strats:
        game = Game(1000)
    else:
        graphs = famous_strategies.strategies
        game = Game(graphs=graphs)
    game.play()
    return game
