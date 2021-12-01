---
title: "Advent of Code: Year 2020, Day 23"
categories:
  - Blog
tags:
  - Advent of Code
  - Raku
---

This is just trashy, slow code that gets the job done. Not functional, not fast, not clever, and not nice to look at. Anyway, enjoy!

## The Problem

### Part 1

After [yesterday's game of War](https://aaronreidsmith.github.io/blog/advent-of-code-year-2020-day-22/), the crab challenges _us_ to a game! In this game there are 10 labeled cups placed clockwise in a circle (our input). The first cup in our list is our "current cup," and the crab is going to make **100 moves**. Here is how each move works:

- The crab picks up the three cups that are immediately clockwise of the current cup. They are removed from the circle; cup spacing is adjusted as necessary to maintain the circle.
- The crab selects a destination cup: the cup with a label equal to the current cup's label minus one. If this would select one of the cups that was just picked up, the crab will keep subtracting one until it finds a cup that wasn't just picked up. If at any point in this process the value goes below the lowest value on any cup's label, it wraps around to the highest value on any cup's label instead.
- The crab places the cups it just picked up so that they are immediately clockwise of the destination cup. They keep the same order as when they were picked up.
- The crab selects a new current cup: the cup which is immediately clockwise of the current cup.

Here is an example of 10 moves with the input `389125467`:

```
-- move 1 --
cups: (3) 8  9  1  2  5  4  6  7 
pick up: 8, 9, 1
destination: 2

-- move 2 --
cups:  3 (2) 8  9  1  5  4  6  7 
pick up: 8, 9, 1
destination: 7

-- move 3 --
cups:  3  2 (5) 4  6  7  8  9  1 
pick up: 4, 6, 7
destination: 3

-- move 4 --
cups:  7  2  5 (8) 9  1  3  4  6 
pick up: 9, 1, 3
destination: 7

-- move 5 --
cups:  3  2  5  8 (4) 6  7  9  1 
pick up: 6, 7, 9
destination: 3

-- move 6 --
cups:  9  2  5  8  4 (1) 3  6  7 
pick up: 3, 6, 7
destination: 9

-- move 7 --
cups:  7  2  5  8  4  1 (9) 3  6 
pick up: 3, 6, 7
destination: 8

-- move 8 --
cups:  8  3  6  7  4  1  9 (2) 5 
pick up: 5, 8, 3
destination: 1

-- move 9 --
cups:  7  4  1  5  8  3  9  2 (6)
pick up: 7, 4, 1
destination: 5

-- move 10 --
cups: (5) 7  4  1  8  3  9  2  6 
pick up: 7, 4, 1
destination: 3

-- final --
cups:  5 (8) 3  7  4  1  9  2  6 
```

After the crab is done, what order will the cups be in? Starting after the cup labeled 1, collect the other cups' labels clockwise into a single string with no extra characters; each number except `1` should appear exactly once. In the above example, after 10 moves, the cups clockwise from `1` are labeled `9`, `2`, `6`, `5`, and so on, producing `92658374`.

What is the answer after 100 moves with an input of `712643589`?

#### Solution

[GitHub Link](https://github.com/aaronreidsmith/advent-of-code/blob/103fedb13cd88b0e852caed8a1ff951d84bffdac/src/main/raku/2020/day-23.raku)

See below for explanation and any implementation-specific comments.

```
sub MAIN($file) {
    my @ring;
    my ($current, $previous);
    for $file.IO.slurp.comb -> $number {
        $current //= $number.Int;            # [1]
        with $previous {                     # [2]
            @ring[$previous] = $number.Int;
        }
        $previous = $number.Int;
    }
    @ring[$previous] = $current;

    for (^100) {
        my $pointer = $current;
        my %grabbed = %(
            0 => True,
            |(1 .. 3).map({
                $pointer = @ring[$pointer]; # [3]
                $pointer => True;
            }).Hash
        );

        my $destination = $current - 1;
        while %grabbed{$destination}:exists {
            $destination = ($destination - 1) % 10;
        }

        (@ring[$current], @ring[$pointer], @ring[$destination]) = (@ring[$pointer], @ring[$destination], @ring[$current]);

        $current = @ring[$current];
    }

    $current = 1;
    my $output;
    while (($current = @ring[$current]) != 1) {
        $output ~= $current;                    # [4]
    }
    say $output;
}
```

This runs as such:

```
$ raku day-23.raku input.txt
29385746
```

#### Explanation

We use a circularly-linked-list (stored in a list of integers) for this.

Once we have parsed our input, we created the linked list by keeping track of our _current_ and _previous_ cups. Then, for 100 iterations, we "grab" 3 cups (plus 0, which is an empty artifact of the way we fill our list), find the next destination cup by decrementing until we find one in the remaining cups, then swapping all the pointers to insert the three "grabbed" cups. For part one, this is a fairly quick process (~0.36s).

##### Specific Comments

1. The `//` operator returns the left-hand-side if it is defined, otherwise the right-hand side. In combination with the `=` operator, it is the same as `$current = $current.defined ?? $current !! $number`.
2. The `with` operator only enters the block if the variable is defined. This is the same as `if $previous.defined {...}`.
3. I hate that we update an outside variable in a map statement. Makes me cringe, but I wrote it, so guess I can't complain too much.
4. `~` is Raku's concatenate operator. So we are taking the `$output` variable, concatenating `$current` and reassigning to `$output`.

### Part 2

The crab adds almost _a million_ more cups to the game. After the 9 initial ones, we add 999,991 more labeled 10 to 1,000,000. Once he has done that, he hides 2 stars in the cups that will end up in the two spots immediately following the cup labeled `1` after _10 million_ rounds. What is the product of those two cup labels?

#### Solution

[GitHub Link](https://github.com/aaronreidsmith/advent-of-code/blob/103fedb13cd88b0e852caed8a1ff951d84bffdac/src/main/raku/2020/day-23.raku)

See below for explanation and any implementation-specific comments.

```
sub part1($file) {
    my @ring;
    my ($current, $previous);
    for $file.IO.slurp.comb -> $number {
        $current //= $number.Int;
        with $previous {
            @ring[$previous] = $number.Int;
        }
        $previous = $number.Int;
    }
    @ring[$previous] = $current;

    for (^100) {
        my $pointer = $current;
        my %grabbed = %(
            0 => True,
            |(1 .. 3).map({
                $pointer = @ring[$pointer];
                $pointer => True;
            }).Hash
        );

        my $destination = $current - 1;
        while %grabbed{$destination}:exists {
            $destination = ($destination - 1) % 10;
        }

        (@ring[$current], @ring[$pointer], @ring[$destination]) = (@ring[$pointer], @ring[$destination], @ring[$current]);

        $current = @ring[$current];
    }

    $current = 1;
    my $output;
    while (($current = @ring[$current]) != 1) {
        $output ~= $current;
    }
    say $output;
}

sub part2($file) {
    my @ring;
    my ($current, $previous);
    for $file.IO.slurp.comb -> $number {
        $current //= $number.Int;
        with $previous {
            @ring[$previous] = $number.Int;
        }
        $previous = $number.Int;
    }

    for (10..1_000_000) -> $i {
        @ring[$previous] = $i;
        $previous = $i;
    }
    @ring[$previous] = $current;

    for (^10_000_000) {
        my $pointer = $current;
        my %grabbed = %(
            0 => True,
            |(1 .. 3).map({
                $pointer = @ring[$pointer];
                $pointer => True;
            }).Hash
        );

        my $destination = $current - 1;
        while %grabbed{$destination}:exists {
            $destination = ($destination - 1) % 1_000_001;
        }

        my $old             = @ring[$current];
        @ring[$current]     = @ring[$pointer];
        @ring[$pointer]     = @ring[$destination];
        @ring[$destination] = $old;

        $current = @ring[$current];
    }

    say @ring[1] * @ring[@ring[1]];
}

sub MAIN($file, Bool :$p2 = False) {
    $p2 ?? part2($file) !! part1($file);
}
```

This runs as such:

```
$ raku day-23.raku input.txt
29385746

$ raku day-23.raku --p2 input.txt
712643589
```

#### Explanation

As you can see, rather than try to retrofit the code today, I just wrote two functions that are _almost_ exactly the same. The differences are as follows:

1. Part 2 adds the extra cups
2. Part 2 has more iterations
3. Part 2 needs a different modulo to find if a cup is in the valid range
4. Part 2 reassigns the pointers in order rather than all at once
    - Shifting that much data in one step really hurt Raku
5. We output the product of 2 numbers instead of just the order of the cups

There is not too much to dive into with this one since it is the same problem with bigger numbers. It's ugly, and I hate it. And, in contrast to part one, it is slow as all get out; it finishes in 351.32s (almost 6 minutes), which makes it 979 times slower than part one. Yikes.

## Final Thoughts

I am burnt out on this, but I am planning on finishing the week out. I enjoy most of the puzzles, but the blogging is starting to wear on me. 😅 2 more days; we got this!
