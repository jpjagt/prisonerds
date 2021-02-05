"""
A graph is a representation of a strategy for prisoners dilemma.

Here, the action C is represented by digit 1, the action D by digit 2.
This makes indexing next state easier.
"""
import numpy as np

# np.array([
#     [1, 0, 1],
#     [1, 0, 2],
#     [2, 2, 2]
# ])


class Graph:
    def __init__(self, data=None):
        if data is None:
            self.data = np.array([[1, 0, 0]])
            self.mutate()
            self.mutate()
            self.mutate()
        else:
            self.data = data
            self.validate()

    def __getitem__(self, item):
        return self.data.__getitem__(item)

    def clone(self, mutate=False):
        cloned = self.__class__(data=self.data)
        if mutate:
            cloned.mutate()
        return cloned

    def validate(self):
        assert set(self.data[:, 0]) <= {
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

    def mutate_flip_action(self):
        "flip one of the actions in actions column"
        index = self.__random_node()
        self.data[index, 0] = 3 - self.data[index, 0]

    def mutate_moveto_random_if_c(self, new_node_index=None):
        "move to a random node if cooperate on some random node"
        if new_node_index is None:
            new_node_index = self.__random_node()
        index = self.__random_node()  # node to be mutated
        self.data[index, 1] = new_node_index

    def mutate_moveto_random_if_d(self, new_node_index=None):
        "move to a random node if defect on some random node"
        if new_node_index is None:
            new_node_index = self.__random_node()
        index = self.__random_node()  # node to be mutated
        self.data[index, 2] = new_node_index

    def mutate_create_node(self):
        action = np.random.choice([1, 2])
        new_node = np.array(
            [[action, self.__random_node(), self.__random_node()]]
        )
        self.data = np.concatenate((self.data, new_node))

        # should we update existing nodes to reference to this node?
        new_index = self.data.shape[0] - 1
        self.mutate_moveto_random_if_c(new_index)
        self.mutate_moveto_random_if_d(new_index)

    def mutate_remove_node(self):
        if not len(self.data) > 1:
            return
        index = self.__random_node()
        self.data = np.delete(self.data, index, axis=0)

        # cleanup
        mask_above = self.data > index
        mask_equal = self.data == index
        mask_above[:, 0] = 0
        mask_equal[:, 0] = 0
        # shift indices
        self.data[mask_above] -= 1
        # update nodes that referenced to deleted node
        x, y = np.where(mask_equal)
        new_indices = [self.__random_node() for _ in range(len(x))]
        self.data[x, y] = new_indices

    def mutate_swap_nodes(self):
        i1 = self.__random_node()
        i2 = self.__random_node()
        n1 = self.data[i1, :]
        self.data[i1, :] = self.data[i2, :]
        self.data[i2, :] = n1

    def mutate_if(self, func, prob):
        if np.random.rand() < prob:
            func()

    def mutate(self):
        self.mutate_if(self.mutate_flip_action, 0.35)
        self.mutate_if(self.mutate_moveto_random_if_c, 0.35)
        self.mutate_if(self.mutate_moveto_random_if_d, 0.35)
        self.mutate_if(self.mutate_create_node, 0.2)
        self.mutate_if(self.mutate_remove_node, 0.15)
        self.mutate_if(self.mutate_swap_nodes, 0.2)
        self.validate()
