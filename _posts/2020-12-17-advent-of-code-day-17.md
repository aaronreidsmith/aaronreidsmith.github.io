---
title: "Advent of Code: Day 17"
categories:
  - Blog
tags:
  - Advent of Code
  - Python
---

Today was _almost exactly_ like [day 11](https://aaronreidsmith.github.io/blog/advent-of-code-day-11/) except with more dimensions. If you remember from day 11, the Raku solution was so slow that I had to write a Python solution (with the same logic) to get it to finish in a reasonable amount of time. Because of the similarities between today's problem and that one, I only wrote a Python solution today.

## The Problem

### Part 1

The elves back at the North Pole call us about a mysterious phenomenon they are witnessing called Conway Cubes occurring in a pocket dimension.

The pocket dimension consists of an infinite 3D grid. At each `(x, y, z)` coordinate there exists a cube in an active (`#`) or inactive (`.`) state. Every cycle in the phenomenon all the cubes _simultaneously_ look at their 26 neighbors (9 above, 9 below, 8 in-plane) and they change based on the following rules:

- If a cube is **active** and **exactly 2 or 3** of its neighbors are also **active**, the cube remains active. Otherwise, the cube becomes **inactive**.
- If a cube is **inactive** but **exactly 3** of its neighbors are active, the cube becomes **active**. Otherwise, the cube remains **inactive**.

Our input is a 2D grid where the top-left position corresponding to coordinate `(0,0,0)` with some active and some inactive cubes. After 6 cycles of the pattern listed above, how many cubes in the space are **active**?

#### Solution

[GitHub Link](https://github.com/aaronreidsmith/advent-of-code/blob/main/2020/17/python/main.py)

See below for explanation and any implementation-specific comments.

```python
from collections import defaultdict
from itertools import product
import sys


def neighbors(coordinates):
    for diff in product([-1, 0, 1], repeat=len(coordinates)): # [1]
        yield tuple(coordinate + diff[i] for i, coordinate in enumerate(coordinates))


def conway_cubes(initial):
    space = defaultdict(lambda: '.') # [2]
    for x, line in enumerate(initial):
        for y, state in enumerate(line):
            cube = (x, y, 0)
            space[cube] = state

    for _ in range(6):
        active = defaultdict(int) # [3]

        for cube in space:
            if space[cube] == ".":
                continue
            for neighbor in neighbors(cube):
                # We count active cubes with active neighbors so we can
                # activate/deactivate following as necessary in the next loop
                active[neighbor] += 1 if neighbor != cube else 0

        for cube, active_neighbors in active.items():
            if space[cube] == "#" and active_neighbors not in (2, 3):
                space[cube] = "."
            elif space[cube] == "." and active_neighbors == 3:
                space[cube] = "#"

    return sum(state == "#" for state in space.values())


if __name__ == '__main__':
    initial = [line.strip() for line in open(sys.argv[1]).readlines()]
    print(conway_cubes(initial))
```

This runs as such:

```
$ python main.py input.txt
137
```

#### Explanation

The logic here is pretty simple:

1. We have an infinite grid called `space` and we set our initial values in the `(x, y, 0)` plane.
2. For 6 cycles we iterate through the cubes focusing first on _active_ cubes (since the rules apply to active neighbors).
3. Within each cycle we do a second loop to look at our neighbors
  - If a cube is active and fewer than 2 or greater than 3 neighbors are inactive, it becomes inactive.
  - If a cube is inactive and exactly 3 neighbors are active, it becomes active.
4. After 6 cycles of this, we simply sum up the active cubes.

##### Specific Comments

1. `product` is a Python 3.8+ function that is basically the equivalent of Raku's `X` operator. In this case, the `repeat` param means to use the same input `repeat` times. So if `repeat=3`, in this case, it would be the same as `[-1, 0, 1] X [-1, 0, 1] X [-1, 0, 1]`.
2. A `defaultdict` is a great data structure for an infinite grid. Basically, the key to `space` will be a tuple of coordinates, and the value will either be a period or a hash. Since it is a `defaultdict`, if we reference a key that does not exist, it creates it and fills it in with the default value (`'.'`).
3. We also use a `defaultdict` to track our active cubes, with the default being an `int`. This will create new items with the default being `0` (`defaultdict` accepts a _function_, not a _value_, which is why we can't just specify `0`).

### Part 2

Turns out the pocket dimension is actually _four dimensional_. Our input now represents the plane `(x, y, 0, 0)`. How many cubes are active after 6 cycles in 4D?

#### Solution

[GitHub Link](https://github.com/aaronreidsmith/advent-of-code/blob/main/2020/17/python/main.py)

See below for explanation and any implementation-specific comments.

```python
from collections import defaultdict
from itertools import product
import sys


def neighbors(coordinates):
    for diff in product([-1, 0, 1], repeat=len(coordinates)):
        yield tuple(coordinate + diff[i] for i, coordinate in enumerate(coordinates))


def conway_cubes(initial, dimensions):
    space = defaultdict(lambda: '.')
    padding = (0,) * (dimensions - 2)
    for x, line in enumerate(initial):
        for y, state in enumerate(line):
            cube = (x, y) + padding
            space[cube] = state

    for _ in range(6):
        active = defaultdict(int)

        for cube in space:
            if space[cube] == ".":
                continue
            for neighbor in neighbors(cube):
                # We count active cubes with active neighbors so we can
                # activate/deactivate following as necessary in the next loop
                active[neighbor] += 1 if neighbor != cube else 0

        for cube, active_neighbors in active.items():
            if space[cube] == "#" and active_neighbors not in (2, 3):
                space[cube] = "."
            elif space[cube] == "." and active_neighbors == 3:
                space[cube] = "#"

    return sum(state == "#" for state in space.values())


if __name__ == '__main__':
    initial = [line.strip() for line in open(sys.argv[1]).readlines()]
    print(f'Part 1: {conway_cubes(initial, dimensions=3)}')
    print(f'Part 2: {conway_cubes(initial, dimensions=4)}')
```

This runs as such:

```
$ python main.py input.txt
Part 1: 237
Part 2: 2448
```

#### Explanation

The changes here are so small, you may not even notice them:

1. `conway_cubes` now accepts a dimension argument
2. We have a dynamic `padding` variable that adds either 1 or 2 zeros to the supplied `(x, y)` coordinates (rather than hard-coding as we did in part one).
3. We run both parts (CLIs are much easier in Raku, so I don't bother in Python)

That's it!

##### Specific Comments

No specific comments to add because the code barely changed. Luckily the code was generalized enough to handle the new dimension.

## Final Thoughts

I didn't write a Raku solution, but I wonder how fast (or slow) if I wrote one with the same logic. Maybe I will go back and compare one of these days!
