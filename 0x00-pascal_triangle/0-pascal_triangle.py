#!/usr/bin/python3
"""
0-pascal_triangle implements a simple pascal_triangle function.
"""


def pascal_triangle(n):
    """Implements a simple pascals triangle"""
    if n <= 0:
        return []

    i = 1
    out = [[1]]

    while i < n:
        tmp = []
        curr = out[-1]
        tmp.append(curr[0])

        for j in range(len(curr) - 1):
            tmp.append(curr[j] + curr[j+1])

        tmp.append(1)
        out.append([*tmp])
        tmp.clear()
        i += 1

    return out
