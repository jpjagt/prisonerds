import Player from .player
import Graph from .graph

class Game:
    def __init__(self, n_graphs):
        self.graphs = np.array([Graph() for _ in n_graphs])
        self.n_graphs = n_graphs
        self.min_rounds = 10
        self.max_rounds = 100
        self.n_graphs_to_keep = int(0.1 * n_players)

    def score_moves(self, moves):
        # moves[i, :] should be compared with
        # moves[all_except_i, i]
        scores = np.fill(-20, size=moves.shape)
        n = len(moves)
        mask = np.ones(n)
        for i in n:
            mask[i] = 0
            my_moves = moves[i, :]
            their_moves = moves[mask, i]
            my_c = my_moves == 1
            their_c = their_moves == 1
            scores[i, my_c & their_c] = -10
            scores[i, my_c & ~their_c] = -25
            scores[i, ~my_c & their_c] = 0
            mask[i] = 1
        return scores

    def play_round(self, players):
        # moves: Nx(N-1) array
        # where moves[i, j] is action of player i for player j
        moves = np.concatenate([p.play() for p in players])
        scores = self.score_moves(moves)
        return scores

    def play_epoch(self):
        n_rounds = np.random.randint(self.min_rounds, self.max_rounds, size=n_graphs)
        n_opponents = n_graphs - 1
        players = [Player(graph, n_opponents) for graph in self.graphs]
        total_scores = np.zeros(size=(n_graphs, n_opponents))
        for r in range(np.max(n_rounds)):
            round_scores = self.play_round(players)
            total_scores += round_scores
        return total_scores

    def __generate_offspring(self, graph, n_offspring):
        return np.array([graph.clone().mutate() for _ in n_offspring])

    # def evolve_graphs(self, total_scores):
    #     sum_of_scores = total_scores.sum(1)
    #     ranking = np.argsort(sum_of_scores)
    #     graphs_to_keep = ranking[:self.n_graphs_to_keep]
    #     parents = self.graphs[graphs_to_keep]

    #     n_offspring = n_graphs // len(parents)
    #     offspring = np.concatenate([self.__generate_offspring(parent, n_offspring) for parent in parents])
    #     np.random.shuffle(offspring)
    #     self.graphs = offspring[:self.n_graphs]

    def play(self):
        try:
            while True:
                total_scores = self.play_epoch()
                self.evolve_graphs(total_scores)
        except KeyboardInterrupt:
            return self.graphs
