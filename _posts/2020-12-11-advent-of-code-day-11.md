---
title: "Advent of Code: Day 11"
categories:
  - Blog
tags:
  - Advent of Code
  - Raku
---

I am giving myself half credit for today; the solution I came up with _is_ in Raku, but it is an iterative solution. Additionally, this solution is _slow_. In fact, it was so slow that in between runs I was able to write a [Python solution](https://github.com/aaronreidsmith/advent-of-code/blob/main/2020/11/python/main.py) (with the same logic) that ran much faster.

## The Problem

### Part 1

We are trying to plug our phone into the seat-back plug, but the problem is it puts out the wrong _joltage_. We have a handful of adaptors labeled by their output joltage (our input), and our device is rated for 3 jolts above the maximum adaptor joltage. Each adaptor can be plugged into an adaptor 1-, 2-, or 3-jolts below it (i.e., a 4-jolt adaptor can plug into a 1-, 2- or 3-jolt plug).

We are bored on this flight, so, treating the seat-back outlet as zero jolts, we want to find a solution that uses _every_ adaptor we own. Once we have found the right sequence, we want to multiply the number of 1-jolt differences by the number of 3-jolt differences.

#### Solution

[GitHub Link](https://github.com/aaronreidsmith/advent-of-code/blob/main/2020/11/raku/main.raku)

See below for explanation and any implementation-specific comments.

```
enum SeatState <Occupied Empty Floor>;

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
                    return @seat-map[$new-row][$new-col];
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
    @old-state[*;*].grep(* eq Occupied).elems;
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
$ raku main.raku input.txt
2152
```

#### Explanation

##### Specific Comments

### Part 2

#### Solution

[GitHub Link](https://github.com/aaronreidsmith/advent-of-code/blob/main/2020/11/raku/main.raku)

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
$ raku main.raku input.txt
2152

# Part 2
$ raku main.raku --p2 input.txt
1937
```

#### Explanation

##### Specific Comments

## Final Thoughts

