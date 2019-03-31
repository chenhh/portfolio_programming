# -*- coding: utf-8 -*-
"""
Author: Hung-Hsin Chen <chenhh@par.cse.nsysu.edu.tw>
"""

import sys
import numpy as np

def swap_regret():
    size = 5
    weights = np.arange(6, 1, -1)
    experts = np.tile(weights, (size * (size-1), 1))
    print(experts)
    row = 0
    for idx in range(size):
        for jdx in range(size):
            if idx != jdx:
                print(idx, jdx, row)
                experts[row, jdx] += experts[row, idx]
                experts[row, idx] = 0
                row += 1
    print(experts)


def ir_example():
    size = 3
    p = np.array([0.2, 0.3, 0.5])
    experts = np.tile(p, (size * (size - 1), 1))
    print(experts)
    row = 0
    for idx in range(size):
        for jdx in range(size):
            if idx != jdx:
                # print(idx, jdx, row)
                experts[row, jdx] += experts[row, idx]
                experts[row, idx] = 0
                row += 1
    print(experts)
    rel = np.array([1.05, 0.9, 0.98])

    new_weights = np.exp(np.log((experts * rel).sum(axis=1)))
    print(new_weights)
    normalized_experts = new_weights/new_weights.sum()
    print(normalized_experts)


    A = np.array([
        [-normalized_experts[0]-normalized_experts[1],
         normalized_experts[0],
         normalized_experts[1]
         ],
        [normalized_experts[2],
         -normalized_experts[2]-normalized_experts[3],
         normalized_experts[3]
         ],
        [normalized_experts[4],
         normalized_experts[5],
         -normalized_experts[4]-normalized_experts[5]
         ]
    ])
    # https://stackoverflow.com/questions/1835246/how-to-solve-homogeneous-linear-equations-with-numpy
    print(A)
    x = np.linalg.solve(A, np.zeros(3))
    print(x)
    print(np.dot(A,x))

if __name__ == '__main__':
    # swap_regret()
    ir_example()