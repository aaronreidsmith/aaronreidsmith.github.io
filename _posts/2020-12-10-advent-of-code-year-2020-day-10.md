---
title: "Advent of Code: Year 2020, Day 10"
categories:
  - Blog
tags:
  - Advent of Code
  - Raku
---

Part two today _almost_ forced me to use an iterative approach that would require a mutable array. However, I stumbled on a great feature of Raku that let me do it recursively without mutability. See below for details!

## The Problem

### Part 1

We are trying to plug our phone into the seat-back plug, but the problem is it puts out the wrong _joltage_. We have a handful of adaptors labeled by their output joltage (our input), and our device is rated for 3 jolts above the maximum adaptor joltage. Each adaptor can be plugged into an adaptor 1-, 2-, or 3-jolts below it (i.e., a 4-jolt adaptor can plug into a 1-, 2- or 3-jolt plug).

We are bored on this flight, so, treating the seat-back outlet as zero jolts, we want to find a solution that uses _every_ adaptor we own. Once we have found the right sequence, we want to multiply the number of 1-jolt differences by the number of 3-jolt differences.

#### Solution

[GitHub Link](https://github.com/aaronreidsmith/advent-of-code/blob/103fedb13cd88b0e852caed8a1ff951d84bffdac/src/main/raku/2020/day-10.raku)

See below for explanation and any implementation-specific comments.

```
sub find-differences(@joltage, $pointer = 0, @differences = ()) {
    if $pointer == @joltage.elems - 1 {
        @differences;
    } else {
        my $a = @joltage[$pointer];
        my $b = @joltage[$pointer + 1];
        find-differences(@joltage, $pointer + 1, (|@differences, $b - $a));
    }
}

sub MAIN($file) {
    my @adaptors = $file.IO.lines.map(*.Int).sort;
    my $device-joltage = @adaptors.max + 3;
    my @joltage-list = (0, |@adaptors, $device-joltage); # [1]
    my @differences = find-differences(@joltage-list);
    say @differences.grep(* == 1).elems * @differences.grep(* == 3).elems;
}
```

This runs as such:

```
$ raku day-10.raku input.txt
2176
```

#### Explanation

The logic laid out in `MAIN` is pretty clear.

1. We pull out all of our adaptors and sort them by output joltage
2. We find out device voltage (`@adaptors.max + 3`)
3. We make our final joltage list including the outlet (`0`) and our device
4. We find all the differences between each adaptor
5. We multiply the 1-joltage differences by the 3-joltage differences

##### Specific Comments

1. I've used this before, but I wanted to call it out as it is used in a few places in this solution. This is called a [`Slip`](https://docs.raku.org/type/Slip), which basically unpacks a list into the outer list. So this is a way of prepending and appending items to a list at the same time.

### Part 2

Now that we have found the one solution that uses all adaptors, we want to find _all_ possible solutions that will connect our device to the plug. Looking at our adaptors we realize there must be more than a **trillion** ways to arrange them, so we have to be smart about how we approach it.

#### Solution

[GitHub Link](https://github.com/aaronreidsmith/advent-of-code/blob/103fedb13cd88b0e852caed8a1ff951d84bffdac/src/main/raku/2020/day-10.raku)

See below for explanation and any implementation-specific comments.

```
use experimental :cached;

sub find-differences(@joltage-list, $pointer = 0, @differences = ()) {
    if $pointer == @joltage-list.elems - 1 {
        @differences;
    } else {
        my $a = @joltage-list[$pointer];
        my $b = @joltage-list[$pointer + 1];
        find-differences(@joltage-list, $pointer + 1, (|@differences, $b - $a));
    }
}

sub find-paths($current-joltage, @joltage-list) is cached {   # [1]
    given $current-joltage {
        when * == @joltage-list.max { 1 }
        when * ∉ @joltage-list      { 0 }                     # [2][3]
        default {
            find-paths($current-joltage + 1, @joltage-list) +
            find-paths($current-joltage + 2, @joltage-list) + # [4]
            find-paths($current-joltage + 3, @joltage-list);
        }
    }
}

sub MAIN($file, Bool :$p2 = False) {
    my @adaptors = $file.IO.lines.map(*.Int).sort;
    my $device-joltage = @adaptors.max + 3;
    my @joltage-list = (0, |@adaptors, $device-joltage);
    if $p2 {
        say find-paths(0, @joltage-list);
    } else {
        my @differences = find-differences(@joltage-list);
        say @differences.grep(* == 1).elems * @differences.grep(* == 3).elems;
    }
}
```

This runs as such:

```
# Part 1
$ raku day-10.raku input.txt
2176

# Part 2
$ raku day-10.raku --p2 input.txt
18512297918464
```

#### Explanation

There is a lot of fluff going on from part one that we can ignore. We generate the same `@joltage-list` and pass it to `find-paths` starting at `joltage = 0`. This subroutine does the following:

1. If we have hit the max joltage (device joltage) mark this as a valid path (`1`)
2. If the joltage we are currently on is not in the set of adaptors, mark it as invalid (`0`)
3. Otherwise, recursively find the valid paths for any adaptors that could plug into this one (i.e. `n+1`, `n+2`, and `n+3`) and add them up

This looks pretty brute-force, right? Well, that is where the `is cached` trait comes in. See #1 below for details!

##### Specific Comments

1. Coming from a Python background, I am familiar with [`functools.cache`](https://docs.python.org/3/library/functools.html#functools.cache), a decorator that basically builds a dictionary of input to output such that expensive functions are only calculated once. Basically, the first call would compute the value and store it in the cache and any subsequent calls to that functions with the same input would use the cached value instead; this optimization is called [memoization](https://en.wikipedia.org/wiki/Memoization). In Raku, this is an [experimental trait](https://docs.raku.org/language/experimental#cached) called `cached` which can be applied to subroutines to achieve the same memoization goal. Basically, the reason this is not a brute-force approach is because we will only compute `find-paths` once for each input rather than the traditional re-computing that can happen in recursive functions.
2. This is the first time using this operator, so I want to call it out: `∉` is the "element not part of set" operator.
3. This function could be optimized by _only_ looking at joltages in the input list, but instead we just look at everything from `0..N`. If it is not in the input list, we just mark it as an invalid path.
4. Because `find-paths($current-joltage + 1, @joltage-list)` will recursively call more `find-paths` functions, this line uses the cache, so the only operation really happening here is the addition.

## Final Thoughts

A lot of my solutions for the Advent of Code so far have been recursive (and relatively slow). I am glad I found out about the `is cached` trait, and I am looking forward to applying it to more solutions in the future!