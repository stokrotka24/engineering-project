import math
import shelve

import numpy as np

from measures import cosine_distance

# from scipy.spatial.distance import cosine as cosine_distance

with shelve.open("../utility_matrix") as f:
    utility_matrix = f["utility_matrix"]

print(type(utility_matrix))
no_cols = utility_matrix.shape[1]
for i in range(1, no_cols):
    min_cosine_dist = math.inf
    column_index = 0
    column_indexes = []
    for j in range(1, no_cols):
        # print(j)
        if i != j:
            dist = cosine_distance(utility_matrix[:, i], utility_matrix[:, j])
            if dist < 1:
                column_indexes.append(j)
            if dist < min_cosine_dist:
                min_cosine_dist = dist
                column_index = j
    # print(column_index)
    # print(column_indexes)
    break

# a = utility_matrix[:, 1]
# b = utility_matrix[:, 2746]
# print(a)
# print(b)
# for (index, val) in enumerate(a):
#     if val != 0 and b[index] != 0:
#         print(f"a[{index}] = {a[index]}")
#         print(f"b[{index}] = {b[index]}")
#         print("-------------------------")
# print(cosine_distance(a, b))
