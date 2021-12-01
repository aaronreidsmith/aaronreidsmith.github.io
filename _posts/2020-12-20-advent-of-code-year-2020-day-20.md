---
title: "Advent of Code: Year 2020, Day 20"
categories:
  - Blog
tags:
  - Advent of Code
  - Python
---

Today was... not fun, to say the very least. It was a lot of tedium, and I am not super proud of my solution.

Today involved a lot of matrix operations. I attempted to use Raku's [Math::Matrix](https://github.com/lichtkind/Raku-Math-Matrix), but found the features to be lacking; I don't know what I expected from a package that hasn't had a release in 2+ years. Instead, this solution was written using [NumPy](https://numpy.org/), a package which I am familiar with, but is not in my day-to-day rotation, so I am sure there is a better solution than mine out there.

## The Problem

### Part 1

The messages from [yesterday](https://aaronreidsmith.github.io/blog/advent-of-code-year-2020-day-19/) decode into a series of images that we need to reassemble back into a single image.

Each of our inputs comes with an ID and the image itself. Here is an example of nine tiles of input:

```
Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###...
```

Unfortunately, it seems the camera was malfunctioning, so these images may be **flipped** or **rotated**. We can find the way these fit together by aligning the borders of adjacent tiles. Here are the above nine tiles flipped and rotated until they fit together:

```
#...##.#.. ..###..### #.#.#####.
..#.#..#.# ###...#.#. .#..######
.###....#. ..#....#.. ..#.......
###.##.##. .#.#.#..## ######....
.###.##### ##...#.### ####.#..#.
.##.#....# ##.##.###. .#...#.##.
#...###### ####.#...# #.#####.##
.....#..## #...##..#. ..#.###...
#.####...# ##..#..... ..#.......
#.##...##. ..##.#..#. ..#.###...

#.##...##. ..##.#..#. ..#.###...
##..#.##.. ..#..###.# ##.##....#
##.####... .#.####.#. ..#.###..#
####.#.#.. ...#.##### ###.#..###
.#.####... ...##..##. .######.##
.##..##.#. ....#...## #.#.#.#...
....#..#.# #.#.#.##.# #.###.###.
..#.#..... .#.##.#..# #.###.##..
####.#.... .#..#.##.. .######...
...#.#.#.# ###.##.#.. .##...####

...#.#.#.# ###.##.#.. .##...####
..#.#.###. ..##.##.## #..#.##..#
..####.### ##.#...##. .#.#..#.##
#..#.#..#. ...#.#.#.. .####.###.
.#..####.# #..#.#.#.# ####.###..
.#####..## #####...#. .##....##.
##.##..#.. ..#...#... .####...#.
#.#.###... .##..##... .####.##.#
#...###... ..##...#.. ...#..####
..#.#....# ##.#.#.... ...##.....
```

With the corresponding tile IDs being:

```
1951    2311    3079
2729    1427    2473
2971    1489    1171
```

To confirm we put the image together correctly, we need to multiply the IDs of the four corners. In this case we get:

```
1951 * 3079 * 2971 * 1171 = 20899048083289
```

What is the product of the four corners in our real input?

#### Solution

[GitHub Link](https://github.com/aaronreidsmith/advent-of-code/blob/103fedb13cd88b0e852caed8a1ff951d84bffdac/src/main/python/2020/day20.py)

See below for explanation and any implementation-specific comments.

```python
import sys

import numpy as np


def orientations(tile):
    for rotation in range(4):
        new_tile = np.rot90(tile, k=rotation)
        yield new_tile                        # [1]
        yield np.flip(new_tile, 1)


if __name__ == '__main__':
    tiles = {}
    for block in open(sys.argv[1]).read().split('\n\n'):
        lines = block.splitlines()
        tile_id = int(lines[0].split(' ')[1][:-1])
        tile = np.array([list(line) for line in lines[1:]]) == '#'  # [2]
        tiles[tile_id] = tile

    grid_width = int(np.sqrt(len(tiles)))

    combined_tiles = []
    found_all_matches = False
    for start_tile_id in tiles.keys():
        for start_tile in orientations(tiles[start_tile_id]):
            combined_tiles = [(start_tile_id, start_tile)]
            used = {start_tile_id}                            # [3]
            found_all_matches = True
            for i in range(1, len(tiles)):
                found_match = False
                for tile_num, tile in tiles.items():
                    if tile_num in used:
                        continue

                    previous_horizontal = combined_tiles[i - 1][1] if i % grid_width != 0 else None
                    previous_vertical = combined_tiles[i - grid_width][1] if i // grid_width != 0 else None

                    for try_tile in orientations(tile):
                        if previous_horizontal is not None and not np.all(previous_horizontal[:, -1] == try_tile[:, 0]):
                            continue
                        if previous_vertical is not None and not np.all(previous_vertical[-1, :] == try_tile[0, :]):
                            continue

                        combined_tiles.append((tile_num, try_tile))
                        used.add(tile_num)
                        found_match = True
                        break

                if not found_match:
                    found_all_matches = False
                    break

            if found_all_matches:
                break

        if found_all_matches:
            break

    tile_ids = np.array([entry[0] for entry in combined_tiles]).reshape((grid_width, grid_width))  # [4]
    corner_product = tile_ids[0, 0] * tile_ids[0, -1] * tile_ids[-1, 0] * tile_ids[-1, -1]
    print(corner_product)
```

This runs as such:

```
$ python day20.py input.txt
23497974998093
```

#### Explanation

First things first, you can see this is an absolute travesty from a time complexity standpoint. I count 5 nested for-loops, making this _O(n<sup>5</sup>)_, which falls squarely in the [horrible category](https://www.bigocheatsheet.com/). Regardless, it runs in under five seconds, so it's not a huge deal. Just wanted to acknowledge that I _know_ it is bad.

The logic for this mess is as follows:

1. First, parse the input into a dictionary with the ID as the key, and a 2D NumPy array as the value
  - We translate `.` and `#` to `True` and `False` on the way in
2. We start with a random tile and iterate through it's orientations
  - 3 rotations (plus the un-rotated version) as well as one flip for each rotation
  - For each rotation we look for the possible matches on all four edges
  - When we find one that fits, we store it in `combined_tiles` and keep looking
  - When we run into one that doesn't fit, we start the whole process over
3. Once we have put all the pieces in their place, we extract _just_ the tile IDs into a grid (like in the example) and multiply the corners.

If it's stupid, but it works, it ain't stupid 🤷🏻‍♂️

##### Specific Comments

1. For anyone not familiar with the `yield` keyword, it is what's known as a `generator` in Python (a lazy list in Raku). Basically, this iterable is only evaluated _when it is asked for_, so all that is stored in memory is how to generate the next term, not anything else. Additionally, generators return to the function _exactly_ where they left off. So after yielding `new_tile` the next term will be the flipped version of `new_tile`. [Here is a link](https://wiki.python.org/moin/Generators) for further reading.
2. NumPy is interesting, so when you have an array compared to a value, it compares each value in the array to that value, and puts it into a new array. This is our way of converting to `True` and `False` values.
3. This defines a `set` with a single item, _not_ a dictionary. Python can be a little confusing on that front:

    ```python
    x = {}               # empty dict
    x = {'foo': 'bar'}   # dict with 1 item
    x = set()            # empty set
    x = {'foo'}          # set with 1 item
    x = set(['foo'])     # also a set with 1 item (`set()` takes an iterable)
    ```

4. `reshape` allows us to convert a list of lists back into an `n x n` matrix.

### Part 2

After putting the image together, we find that it is a picture of the ocean, and it is full of **sea monsters**. First things first, lets take of the borders used to align the pieces. The above example becomes this:

```
.#.#..#. ##...#.# #..#####
###....# .#....#. .#......
##.##.## #.#.#..# #####...
###.#### #...#.## ###.#..#
##.#.... #.##.### #...#.##
...##### ###.#... .#####.#
....#..# ...##..# .#.###..
.####... #..#.... .#......

#..#.##. .#..###. #.##....
#.####.. #.####.# .#.###..
###.#.#. ..#.#### ##.#..##
#.####.. ..##..## ######.#
##..##.# ...#...# .#.#.#..
...#..#. .#.#.##. .###.###
.#.#.... #.##.#.. .###.##.
###.#... #..#.##. ######..

.#.#.### .##.##.# ..#.##..
.####.## #.#...## #.#..#.#
..#.#..# ..#.#.#. ####.###
#..####. ..#.#.#. ###.###.
#####..# ####...# ##....##
#.##..#. .#...#.. ####...#
.#.###.. ##..##.. ####.##.
...###.. .##...#. ..#..###
```

And then we can remove the gaps to be left with a full grid:

```
.#.#..#.##...#.##..#####
###....#.#....#..#......
##.##.###.#.#..######...
###.#####...#.#####.#..#
##.#....#.##.####...#.##
...########.#....#####.#
....#..#...##..#.#.###..
.####...#..#.....#......
#..#.##..#..###.#.##....
#.####..#.####.#.#.###..
###.#.#...#.######.#..##
#.####....##..########.#
##..##.#...#...#.#.#.#..
...#..#..#.#.##..###.###
.#.#....#.##.#...###.##.
###.#...#..#.##.######..
.#.#.###.##.##.#..#.##..
.####.###.#...###.#..#.#
..#.#..#..#.#.#.####.###
#..####...#.#.#.###.###.
#####..#####...###....##
#.##..#..#...#..####...#
.#.###..##..##..####.##.
...###...##...#...#..###
```

We need to find the sea monsters in the above image. They look like this:

```
                  # 
#    ##    ##    ###
 #  #  #  #  #  #   
```

When looking for a sea monster, the spaces can be either `#` or `.`, as long as those specific `#` symbols match. After rotating and flipping the grid, we find two sea monsters (marked as `O` characters):

```
.####...#####..#...###..
#####..#..#.#.####..#.#.
.#.#...#.###...#.##.O#..
#.O.##.OO#.#.OO.##.OOO##
..#O.#O#.O##O..O.#O##.##
...#.#..##.##...#..#..##
#.##.#..#.#..#..##.#.#..
.###.##.....#...###.#...
#.####.#.#....##.#..#.#.
##...#..#....#..#...####
..#.##...###..#.#####..#
....#.##.#.#####....#...
..##.##.###.....#.##..#.
#...#...###..####....##.
.#.##...#.##.#.#.###...#
#.###.#..####...##..#...
#.###...#.##...#.##O###.
.O##.#OO.###OO##..OOO##.
..O#.O..O..O.#O##O##.###
#.#..##.########..#..##.
#.#####..#.#...##..#....
#....##..#.#########..##
#...#.....#..##...###.##
#..###....##.#...##.##.#
```

After identifying the sea monsters, we can calculate how rough the water is by counting the number of remaining `#` characters. In the above example it is `273`; what is the water roughness in our actual input?

#### Solution

[GitHub Link](https://github.com/aaronreidsmith/advent-of-code/blob/103fedb13cd88b0e852caed8a1ff951d84bffdac/src/main/python/2020/day20.py)

See below for explanation and any implementation-specific comments.

```python
import sys

import numpy as np


def orientations(matrix):
    for rotation in range(4):
        new_matrix = np.rot90(matrix, k=rotation)
        yield new_matrix
        yield np.flip(new_matrix, 1)


if __name__ == '__main__':
    tiles = {}
    for block in open(sys.argv[1]).read().split('\n\n'):
        lines = block.splitlines()
        tile_id = int(lines[0].split(' ')[1][:-1])
        tile = np.array([list(line) for line in lines[1:]]) == '#'
        tiles[tile_id] = tile

    grid_width = int(np.sqrt(len(tiles)))

    combined_tiles = []
    found_all_matches = False
    for start_tile_id in tiles.keys():
        for start_tile in orientations(tiles[start_tile_id]):
            combined_tiles = [(start_tile_id, start_tile)]
            used = {start_tile_id}
            found_all_matches = True
            for i in range(1, len(tiles)):
                found_match = False
                for tile_num, tile in tiles.items():
                    if tile_num in used:
                        continue

                    previous_horizontal = combined_tiles[i - 1][1] if i % grid_width != 0 else None
                    previous_vertical = combined_tiles[i - grid_width][1] if i // grid_width != 0 else None

                    for try_tile in orientations(tile):
                        if previous_horizontal is not None and not np.all(previous_horizontal[:, -1] == try_tile[:, 0]):
                            continue
                        if previous_vertical is not None and not np.all(previous_vertical[-1, :] == try_tile[0, :]):
                            continue

                        combined_tiles.append((tile_num, try_tile))
                        used.add(tile_num)
                        found_match = True
                        break

                if not found_match:
                    found_all_matches = False
                    break

            if found_all_matches:
                break

        if found_all_matches:
            break

    final_grid_ids = np.array([entry[0] for entry in combined_tiles]).reshape((grid_width, grid_width))
    corner_product = final_grid_ids[0, 0] * final_grid_ids[0, -1] * final_grid_ids[-1, 0] * final_grid_ids[-1, -1]
    print(f'Part 1: {corner_product}')

    tile_width = combined_tiles[0][1].shape[0] - 2  # Remove borders on each side
    grid = np.zeros((tile_width * grid_width, tile_width * grid_width), dtype=bool)
    for index, (_, tile) in enumerate(combined_tiles):
        row, column = divmod(index, grid_width)
        grid[
            row * tile_width:row * tile_width + tile_width,
            column * tile_width:column * tile_width + tile_width
        ] = tile[1:-1, 1:-1]

    monster = (
        '                  # ',
        '#    ##    ##    ###',
        ' #  #  #  #  #  #   '
    )
    monster = np.array([list(line) for line in monster]) == '#'

    water_roughness = None
    for orientation in orientations(grid):
        num_monsters = 0

        for i in range(grid.shape[0] - monster.shape[0] + 1):
            for j in range(grid.shape[1] - monster.shape[1] + 1):
                grid_slice = orientation[i:i + monster.shape[0], j:j + monster.shape[1]]
                if np.all((grid_slice & monster) == monster):
                    num_monsters += 1

        if num_monsters > 0:
            water_roughness = np.sum(grid) - num_monsters * np.sum(monster)
            break

    print(f'Part 2: {water_roughness}')
```

This runs as such:

```
$ python day20.py input.txt
Part 1: 20899048083289
Part 2: 2256
```

#### Explanation

Immediately where part one left off we apply the following logic:

1. First remove the border from each tile we just aligned
2. Start with an empty grid (`np.zeroes`) and build it up tile-by-tile so that we have an outer matrix full of smaller matrices
3. Define our monster as a NumPy matrix
4. Again, iterate through possible orientations (grid orientations this time) and generate slices the size of a monster
5. Check if the slice _is_ a monster
6. If we found a monster, we must be in the right orientation
7. To find the water roughness we `sum` the whole grid (which will just count the `True` values), then subtract the number of those `True` values that are in a monster `num_monsters - np.sum(monster)`

## Final Thoughts

According to the [creator of Advent of Code](https://www.youtube.com/watch?v=CFWuwNDOnIo), weekend puzzles are intentionally harder because that is when people have time to do them. With that in mind, I am hoping the rest of the puzzles are easier than today! If I can't have that, then I at least hope they are less tedious. 🙂 Just five more days!
