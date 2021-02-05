from graph import Graph
import numpy as np

# https://www.researchgate.net/publication/259354712_Forgiver_Triumphs_in_Alternating_Prisoner's_Dilemma

S4 = np.array([[2, 0, 1], [1, 1, 0]])
S8 = np.array([[2, 1, 0], [1, 1, 0]])
S12 = np.array([[2, 1, 1], [1, 1, 0]])
S14 = np.array([[1, 0, 1], [2, 0, 0]])
S15 = np.array([[1, 0, 1], [2, 0, 1]])
S16 = np.array([[1, 0, 1], [2, 1, 0]])
S17 = np.array([[1, 0, 1], [2, 1, 1]])
S21 = np.array([[1, 1, 0], [2, 1, 1]])
S25 = np.array([[1, 1, 1], [2, 0, 0]])
S10 = np.array([[2, 1, 1], [1, 0, 0]])

strat_arrs = [S4, S8, S12, S14, S15, S16, S17, S21, S25, S10]
strategies = [Graph(s) for s in strat_arrs]
