---
title: "Advent of Code: Year 2020, Day 11"
categories:
  - Blog
tags:
  - Advent of Code
  - Raku
  - Python
---

I am giving myself half credit for today; the solution I came up with _is_ in Raku, but it is an iterative solution. Additionally, this solution is _slow_. In fact, it was so slow that in between runs I was able to write a [Python solution](https://github.com/aaronreidsmith/advent-of-code/blob/103fedb13cd88b0e852caed8a1ff951d84bffdac/src/main/python/2020/day11.py) (with the same logic) that ran much faster.

## The Problem

### Part 1

We finally landed, and the last leg of our journey is via ferry, and we are all spilling into the waiting area right now. We are trying to find the best place to sit, so we make a quick sketch of the seat map in the waiting area (our input). Here is an example:

```
L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL
```	

Each position is either floor (`.`), an empty seat (`L`) or an occupied seat (`#`).

We are apparently traveling with a bunch of psychopaths who adhere to the following rules when finding a seat. For these rules the term "neighbor" is used to describe any of the eight seats (vertically, horizontally, and diagonally) immediately adjacent to the target chair. 

- If the seat is empty and zero neighbors are occupied, the seat becomes occupied
- If the seat is occupied and four or more neighbors are occupied, the seat becomes empty
- Otherwise, the seat stays the same.

The interesting thing about the layout is that (following the above rules) it will _eventually_ reach a steady state. How many seats are occupied when it reaches steady state?

#### Solution

[GitHub Link](https://github.com/aaronreidsmith/advent-of-code/blob/103fedb13cd88b0e852caed8a1ff951d84bffdac/src/main/raku/2020/day-11.raku)

See below for explanation and any implementation-specific comments.

```
enum SeatState <Occupied Empty Floor>; # [1]

sub find-equilibrium(@state) {
    my ($max-row, $max-col) = @state.elems, @state[0].elems;
    my @directions = (
        (-1, 0), # N
        (-1, 1), # NE
        (0, 1),  # E
        (1, 1),  # SE
        (1, 0),  # S
        (1, -1), # SW
        (0, -1), # W
        (-1, -1) # NW
    );

    sub occupied-neighbors(@seat-map, $row, $col) {
        sub neighbor(@direction) {
            my ($new-row, $new-col) = $row, $col;
            loop {
                $new-row += @direction[0];
                $new-col += @direction[1];
                if ($new-row < 0 || $new-row >= $max-row || $new-col < 0 || $new-col >= $max-col) {
                    return 'Out of Bounds';
                } else {
                    return @seat-map[$new-row][$new-col]; # [2]
                }
            }
        }
        @directions.map(&neighbor).grep(* eq Occupied).elems;
    }

    my @old-state;
    while @old-state ne @state {
        @old-state = @state;
        @state = ();
        for ^$max-row -> $row {
            my @new-row;
            for ^$max-col -> $col {
                my $current-seat = @old-state[$row][$col];
                my $occupied-neighbors = occupied-neighbors(@old-state, $row, $col);
                if $current-seat eq Empty && $occupied-neighbors == 0 {
                    @new-row.push(Occupied);
                } elsif $current-seat eq Occupied && $occupied-neighbors >= 4 {
                    @new-row.push(Empty);
                } else {
                    @new-row.push($current-seat);
                }
            }
            @state.push(@new-row);
        }
    }
    @old-state[*;*].grep(* eq Occupied).elems; # [3][4]
}


sub MAIN($file) {
    my @seats = $file.IO.lines.map(-> $line {
        $line.comb.map(-> $char {
            given $char {
                when '#' { Occupied }
                when 'L' { Empty }
                when '.' { Floor }
            }
        })
    });
    say find-equilibrium(@seats);
}
```

This runs as such:

```
$ raku day-11.raku input.txt
2152
```

#### Explanation

The logic here is basically as follows:

1. First, make a 2D array of the input, where each cell is a valid `SeatState` (no use passing those cryptic characters around) and pass that to the `find-equilibrium` subroutine.
2. In the `find-equilibrium` subroutine, we basically iterate until `@old-state` equals `@state`.
3. For each cell we find count the occupied neighbors and the apply the rules (by comparing to `@old-state`):
  - If the current seat is`Empty` and the neighbors areall `Empty`, make it `Occupied`.
  - If the current seat is `Occupied` and four or more neighbors are `Occupied`, make it `Empty`.
  - Otherwise, leave it alone.
4. Finally, we count up the occupied cells.

##### Specific Comments

1. I just used an `enum` for clarity when reading this; it makes it a lot easier to understand than something like `if $seat eq '#'`.
2. This is one of the few times you will see me use an explicit `return` in Raku (especially functional Raku). In general, the last statement evaluated in the block is the return value. But, since we have an infinite `loop`, we have to add the explicit `return` statements here.
3. This is the Raku way to [flatten a 2D list](https://docs.raku.org/language/subscripts#index-entry-flattening_). If it were a 3D list, we would do `@list[*;*;*]`.
4. `==` is only used for numbers in Raku; everything else should us `eq`, `ne`, etc.

### Part 2

We realize that the pattern the pattern the waiting passengers is following is not actually as simple as we made it.

They are actually looking for the _first seat they can see_ in all eight directions rather than just the eight adjacent chairs. For example, the empty chair below would see eight occupied seats:

```
.......#.
...#.....
.#.......
.........
..#L....#
....#....
.........
#........
...#.....
```

Additionally, people seem to be more tolerant than expected and will only vacate their seat if **five or more** occupied seats are visible. How many seats are occupied at steady state now?

#### Solution

[GitHub Link](https://github.com/aaronreidsmith/advent-of-code/blob/103fedb13cd88b0e852caed8a1ff951d84bffdac/src/main/raku/2020/day-11.rakuu)

See below for explanation and any implementation-specific comments.

```
enum SeatState <Occupied Empty Floor>;

sub find-equilibrium(@state, Int $min-occupied, Bool $only-immediate) {
    my ($max-row, $max-col) = @state.elems, @state[0].elems;
    my @directions = (
        (-1, 0), # N
        (-1, 1), # NE
        (0, 1),  # E
        (1, 1),  # SE
        (1, 0),  # S
        (1, -1), # SW
        (0, -1), # W
        (-1, -1) # NW
    );

    sub occupied-neighbors(@seat-map, $row, $col) {
        sub neighbor(@direction) {
            my ($new-row, $new-col) = $row, $col;
            my $valid-seats = Set[SeatState].new(Occupied, Empty);
            loop {
                $new-row += @direction[0];
                $new-col += @direction[1];
                if ($new-row < 0 || $new-row >= $max-row || $new-col < 0 || $new-col >= $max-col) {
                    return 'Out of Bounds';
                } else {
                    my $seat = @seat-map[$new-row][$new-col];
                    if $seat ∈ $valid-seats || $only-immediate {
                        return $seat;
                    }
                }
            }
        }
        @directions.map(&neighbor).grep(* eq Occupied).elems;
    }

    my @old-state;
    while @old-state ne @state {
        @old-state = @state;
        @state = ();
        for ^$max-row -> $row {
            my @new-row;
            for ^$max-col -> $col {
                my $current-seat = @old-state[$row][$col];
                my $occupied-neighbors = occupied-neighbors(@old-state, $row, $col);
                if $current-seat eq Empty && $occupied-neighbors == 0 {
                    @new-row.push(Occupied);
                } elsif $current-seat eq Occupied && $occupied-neighbors >= $min-occupied {
                    @new-row.push(Empty);
                } else {
                    @new-row.push($current-seat);
                }
            }
            @state.push(@new-row);
        }
    }
    @old-state[*;*].grep(* eq Occupied).elems;
}


sub MAIN($file, Bool :$p2 = False) {
    my @seats = $file.IO.lines.map(-> $line {
        $line.comb.map(-> $char {
            given $char {
                when '#' { Occupied }
                when 'L' { Empty }
                when '.' { Floor }
            }
        })
    });
    my $min-occupied = $p2 ?? 5 !! 4;
    my $only-immediate = !$p2;
    say find-equilibrium(@seats, $min-occupied, $only-immediate);
}
```

This runs as such:

```
# Part 1
$ raku day-11.raku input.txt
2152

# Part 2
$ raku day-11.raku --p2 input.txt
1937
```

#### Explanation

This code looks almost the same. Here are the _only_ changes to the code:

1. `find-equilibrium` now takes two additional parameters:
	- `$min-occupied`: How many nearby seats need to be occupied for someone to vacate theirs.
	- `$only-immediate`: Whether or not we should only look at the eight immediate neighbors.
2. The `elsif` block has been changed to utilize `$min-occupied` instead of being hard-coded to `4`.
3. The `MAIN` subroutine will define `$min-occupied` as `5` if it's part two, otherwise `4`.
4. The `MAIN` subroutine will define `$only-immediate` as `False` if it's part two, otherwise `True`.

That's it!

##### Specific Comments

Nothing for part two!

## Final Thoughts

This solution is just begging to be done iteratively, so I can't blame myself too much for naturally leaning towards an iterative approach. With that being said, I would love to see some functional approaches to this just to better my understanding of the functional mindset.

