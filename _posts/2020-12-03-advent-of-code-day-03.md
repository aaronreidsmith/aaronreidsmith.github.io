---
title: "Advent of Code: Day 3"
categories:
  - Blog
tags:
  - Advent of Code
  - Raku
---

Today was the first problem that I felt lent itself naturally to a for-loop. While there is nothing wrong with a [for-loop in functional programming programming](https://two-wrongs.com/myth-of-the-day-functional-programmers-dont-use-loops), I wanted to used one of the common substitutes in the functional programmer's tool belt: recursion.


## The Problem

### Part 1

We are going sledding this week! Our job is to get to the bottom of the mountain following a specific path, and to count how many trees we would run into along the way.

Given a file that looks like the diagram below, we are to start in the top left of this file and traverse right three spaces and down one space until we hit the bottom, counting the number of hash signs (trees) we encounter.

```
...#..............#.#....#..#..
...#..#..#..............#..#...
```

Additionally, this is a magic mountain, so the pattern on each row repeats out to the right infinitely, and we have to account for that.


#### Solution

[GitHub Link](https://github.com/aaronreidsmith/advent-of-code/blob/main/2020/03/raku/main.raku)

See below for explanation and any implementation-specific comments.

```
sub traverse(@mountain, $trees-encountered = 0, $i = 0, $j = 0) {
    if $i > @mountain.elems - 1 {
        $trees-encountered;
    } else {
        my $tree-hit = @mountain[$i][$j] cmp '#' == Same ?? 1 !! 0;
        if $i == @mountain.elems - 1 {
            $trees-encountered + $tree-hit;
        } else {
            traverse(@mountain, $trees-encountered + $tree-hit, $i + 1, $j + 3);
        }
    }
}

sub MAIN($file) {
    say traverse($file.IO.lines.map(-> $line { |$line.comb xx * })); # [1][2][3][4]
}
```

This runs as such:

```
$ raku main.raku input.txt
191
```

#### Explanation

Other than the below comments, I feel like this reads fairly easily. Basically, we turn our file into a list of infinite lists (described below) and then call `traverse` on that outer list. `traverse` is a [tail-recursive](https://www.geeksforgeeks.org/tail-recursion/) function with fairly simple logic:

  - If we have already passed the bottom, return the number of trees we hit
  - If we are at the bottom of the mountain, see if we are currently hitting a tree and then return `$trees-encountered` with the last tree included
  - Otherwise, add the current tree hit to `$trees-encountered` and go down one row and to the right three columns

##### Specific Comments

1. `|` has a special meaning when used in front of a list. It flattens any inner lists to the top level. So, for example, if we had `|((1, 2), (3, 4))`, that would equal `(1, 2, 3, 4)`.
2. Reminder that `.comb` splits the input into a list of characters.
3. `xx` is a special operator that takes the input list and concatenates it to itself `N` times (`N = *` here; see below). So, for example, if we had `(1, 2) xx 2`, that would yield `((1, 2), (1, 2))`.
4. `xx` allows the [`Whatever`](https://docs.raku.org/type/Whatever) character (`*`) on the right-hand side, and in that case it returns a lazy, infinite concatenation of the left-hand side.

So, to summarize the above comments, we take the line and `comb` it to a list. Then, we concatenate that list infinitely to have a list of lists, which we flatten using the `|` operator. Since this happens in a `map`, it applies to each line, so we have one finite outer list containing multiple infinite lists. We then traverse the outer list.

### Part 2

Given the same file as before, we want to tackle it with five different traversals:

- Right 1, down 1
- Right 3, down 1 (This is the slope we already checked)
- Right 5, down 1
- Right 7, down 1
- Right 1, down 2

Then, we must find the product of all the trees we hit with each traversal

#### Solution

[GitHub Link](https://github.com/aaronreidsmith/advent-of-code/blob/main/2020/03/raku/main.raku)

See below for explanation and any implementation-specific comments.

```
sub traverse(@mountain, $i-increment, $j-increment, $trees-encountered = 0, $i = 0, $j = 0) {
    if $i > @mountain.elems - 1 {
        $trees-encountered;
    } else {
        my $tree-hit = @mountain[$i][$j] cmp '#' == Same ?? 1 !! 0;
        if $i == @mountain.elems - 1 {
            $trees-encountered + $tree-hit;
        } else {
            traverse(
                @mountain,
                $i-increment,
                $j-increment,
                $trees-encountered + $tree-hit,
                $i + $i-increment,
                $j + $j-increment
            );
        }
    }
}

sub MAIN($file, Bool :$p2 = False) {
    my @traversals = $p2 ?? (
        (1, 1),
        (1, 3),
        (1, 5),
        (1, 7),
        (2, 1)      # [1]
    ) !! ((1, 3),); # [2]
    say [*] @traversals.map(-> ($i-increment, $j-increment) {
        traverse($file.IO.lines.map(-> $line { |$line.comb xx * }), $i-increment, $j-increment)
    });
}
```

This runs as such:

```
# Part 1
$ raku main.raku input.txt
191

# Part 2
$ raku main.raku --p2 input.txt
1478615040
```

#### Explanation

Again, we are able to tweak our code slightly and handle both parts one and two in one block. In this case, we added two arguments to `traverse` to tell it the row step-size and column step-size. We then just add the list of lists corresponding to the five traversals noted above, `map` over them and calculate the product using the `[*]` operator! In the case of part one, it is a list of size one, so `[*]` will just return the single element.

##### Specific Comments

1. The input file has 323 lines, so we will hit the `$i > @mountain.elems - 1` case with this traversal, so it is a good thing we generalized it in the previous step!
2. Need this to be a list of lists to map over it, so we need the comma to denote the outer list is of size one.


## Final Thoughts

I felt this problem came very serendipitously; I was _just_ reading about the `|` and `xx` operators last night, so I am glad I got to put them to use. Recursion (and more specifically tail recursion) is always a fun approach, and it let us tackle this problem functionally. 3 for 3! Let's see what tomorrow brings.