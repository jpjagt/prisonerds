"""
A graph is a representation of a strategy for prisoners dilemma.

Here, the action C is represented by digit 1, the action D by digit 2.
This makes indexing next state easier.
"""
import numpy as np


class Graph:
    def __init__(self, data=None):
        self.data = data or np.array([[1, 0, 0]])
        if data is None:
            self.mutate()
            self.mutate()
            self.mutate()

    def __getitem__(self, item):
        return self.data.__getitem__(item)

    def clone(self):
        return self.__class__(data=self.data)

    def validate(self):
        assert set(self.data[:, 0]) == {
            1,
            2,
        }, "actions column contains forbidden values"
        n_nodes = self.data.shape[0]
        assert (
            self.data[:, 1].max() < n_nodes
        ), "reference to non-existing node"
        assert self.data[:, 1].min() >= 0, "reference to non-existing node"
        assert (
            self.data[:, 2].max() < n_nodes
        ), "reference to non-existing node"
        assert self.data[:, 2].min() >= 0, "reference to non-existing node"

    def __random_node(self):
        return np.random.randint(self.data.shape[0])

    def __mutate_flip_action(self):
        "flip one of the actions in actions column"
        index = self.__random_node()
        self.data[index, 0] = 3 - self.data[index, 0]

    def __mutate_moveto_random_if_c(self, new_node_index=None):
        "move to a random node if cooperate on some random node"
        if new_node_index is None:
            new_node_index = self.__random_node()
        index = self.__random_node()  # node to be mutated
        self.data[index, 1] = new_node_index

    def __mutate_moveto_random_if_d(self, new_node_index=None):
        "move to a random node if defect on some random node"
        if new_node_index is None:
            new_node_index = self.__random_node()
        index = self.__random_node()  # node to be mutated
        self.data[index, 2] = new_node_index

    def __mutate_create_node(self):
        action = np.random.choice([1, 2])
        new_node = np.array(
            [[action, self.__random_node(), self.__random_node()]]
        )
        self.data = np.concatenate((self.data, new_node))

        # should we update existing nodes to reference to this node?
        new_index = self.data.shape[0] - 1
        self.__mutate_moveto_random_if_c(new_index)
        self.__mutate_moveto_random_if_d(new_index)

    def __mutate_remove_node(self):
        index = self.__random_node()
        self.data = np.delete(self.data, index, axis=0)

        # cleanup
        data_without_actions = self.data[:, :]
        data_without_actions[:, 0] = -1
        # update nodes that referenced to deleted node
        x, y = data_without_actions == index
        new_indices = [self.__random_node() for _ in len(x)]
        self.data[x, y] = new_indices
        # shift indices
        mask = data_without_index > index
        self.data[mask] -= 1

    def __mutate_swap_nodes(self):
        i1 = self.__random_node()
        i2 = self.__random_node()
        n1 = self.data[i1, :]
        self.data[i1, :] = self.data[i2, :]
        self.data[i2, :] = n1

    def __mutate_if(func, prob):
        if np.random.rand() < prob:
            func()

    def mutate(self):
        self.__mutate_if(self.__mutate_flip_action, 0.25)
        self.__mutate_if(self.__mutate_moveto_random_if_c, 0.25)
        self.__mutate_if(self.__mutate_moveto_random_if_d, 0.25)
        self.__mutate_if(self.__mutate_create_node, 0.05)
        self.__mutate_if(self.__mutate_remove_node, 0.05)
        self.__mutate_if(self.__mutate_swap_nodes, 0.1)
        self.validate()
