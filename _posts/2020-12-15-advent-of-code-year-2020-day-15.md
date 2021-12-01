---
title: "Advent of Code: Year 2020, Day 15"
categories:
  - Blog
tags:
  - Advent of Code
  - Raku
---

Even with how short and sweet today's solution is, I had to rewrite it between parts one and two after hitting the maximum recursion depth. So we've got one functional, recursive solution and one imperative, iterative solution!

## The Problem

### Part 1

While we wait for our next flight, we decide to call the elves back at the North Pole. They're playing a memory game that they want us to join.

In this game, the players take turns saying numbers. They begin by taking turns reading from a list of starting numbers (your puzzle input). Then, each turn consists of considering the most recently spoken number:

- If that was the first time the number has been spoken, the current player says `0`.
- Otherwise, the number had been spoken before; the current player announces how many turns apart the number is from when it was previously spoken.

Here is an example with input `0,3,6`:

- Turn 1: The 1st number spoken is a starting number, `0`.
- Turn 2: The 2nd number spoken is a starting number, `3`.
- Turn 3: The 3rd number spoken is a starting number, `6`.
- Turn 4: Now, consider the last number spoken, `6`. Since that was the first time the number had been spoken, the 4th number spoken is `0`.
- Turn 5: Next, again consider the last number spoken, `0`. Since it had been spoken before, the next number to speak is the difference between the turn number when it was last spoken (the previous turn, 4) and the turn number of the time it was most recently spoken before then (turn 1). Thus, the 5th number spoken is 4 - 1, `3`.
- Turn 6: The last number spoken, `3` had also been spoken before, most recently on turns `5` and `2`. So, the 6th number spoken is 5 - 2, `3`.
- Turn 7: Since 3 was just spoken twice in a row, and the last two turns are 1 turn apart, the 7th number spoken is `1`.
- Turn 8: Since 1 is new, the 8th number spoken is `0`.
- Turn 9: `0` was last spoken on turns 8 and 4, so the 9th number spoken is the difference between them, `4`.
- Turn 10: `4` is new, so the 10th number spoken is `0`.

Given an input of `11,18,0,20,1,7,16`, what will be the 2020<sup>th</sup> number?

#### Solution

[GitHub Link](https://github.com/aaronreidsmith/advent-of-code/blob/103fedb13cd88b0e852caed8a1ff951d84bffdac/src/main/raku/2020/day-15.raku)

See below for explanation and any implementation-specific comments.

```
sub play-game(%numbers, $turn, $number, $target-turn) {
    if $turn == $target-turn {
        $number;
    } else {
        my $next-number = %numbers{$number}:exists ?? $turn - %numbers{$number} !! 0;        # [1]
        play-game(%(|%numbers, |($number => $turn)), $turn + 1, $next-number, $target-turn); # [2]
    }
}

sub MAIN($file, Bool :$p2 = False) {
    my %initial = $file.IO.slurp.split(',').kv.map(-> $key, $value { $value => $key + 1 } ).Hash;
    say play-game(%initial, %initial.elems + 1, 0, 2020);
}
```

This runs as such:

```
$ raku day-15.raku input.txt
639
```

#### Explanation

So, in `MAIN` we first pull everything from our input into a `Hash` with the keys being the number that was said by the elves, and the value being the turn it was said on. Then we pass that to `play-game` with four parameters: 

- The `Hash` itself
- The turn we are starting on (in the case of our input, 8)
- The next number in the sequence (since our input is so small, we can hard-code this to 0)
- The number in the sequence we are hoping to find (2020)

`play-game` will recursively do the following (until it hits turn 2020):

- If we have seen this number find the difference between this turn, and the turn it was last said on, otherwise `0`
- Update the `%numbers` variable with the new number/turn pair

That's it!

##### Specific Comments

1. The `:exists` tag here is something called an [adverb](https://docs.raku.org/language/subscripts#index-entry-:exists_(subscript_adverb)) in Raku. It is the equivalent of `key in dictionary` in Python.
2. There is some special syntax on this line for merging hashes without mutating the original hashes. The slip character (`|`) unpacks the two hashes into an outer `Hash` (denoted by the preceding `%` sigil) and gives precedence to the second `Hash`. Here is what that means in simple terms:

```
my %a = (a => 1, b => 2);  # {a => 1, b => 2} 
my %b = (b => 3, c => 4);  # {b => 3, c => 4}
my %c = %(|%a, |%b);       # {a => 1, b => 3, c => 4}
```

### Part 2

The elves are impressed with our memory skills, so they up the ante! What is the _30 millionth_ term in the sequence?

#### Solution

[GitHub Link](https://github.com/aaronreidsmith/advent-of-code/blob/103fedb13cd88b0e852caed8a1ff951d84bffdac/src/main/raku/2020/day-15.raku)

See below for explanation and any implementation-specific comments.

```
sub play-game-recursive(%numbers, $turn, $number, $target-turn) {
    if $turn == $target-turn {
        $number;
    } else {
        my $next-turn = %numbers{$number}:exists ?? $turn - %numbers{$number} !! 0;
        play-game-recursive(
            %(|%numbers, |($number => $turn)),
            $turn + 1,
            $next-turn,
            $target-turn
        );
    }
}

sub play-game-iterative(%numbers is copy, $target-turn) {                                      # [1]
    my $last-item = %numbers.pairs.sort({ $^a.value cmp $^b.value })[*-1];                     # [2]
    for (%numbers.elems^..$target-turn) -> $turn {                                             # [3]
        my $new-item = %numbers{$last-item}:exists ?? ($turn - 1) - %numbers{$last-item} !! 0;
        %numbers{$last-item} = $turn - 1;
        $last-item = $new-item;
    }
    $last-item;
}

sub MAIN($file, Bool :$p2 = False) {
    my %initial = $file.IO.slurp.split(',').kv.map(-> $key, $value { $value => $key + 1 } ).Hash;
    my $last-turn = $p2 ?? 30_000_000 !! 2020;                                                    # [4]
    say play-game-iterative(%initial, $last-turn);
}
```

This runs as such:

```
# Part 1
$ raku day-15.raku input.txt
639

# Part 2
$ raku day-15.raku --p2 input.txt
266
```

#### Explanation

So the first thing you'll notice is I refactored `play-game` to be called `play-game-recursive`; this is not used anywhere, it was simply left in to show the progression of the code.

`MAIN` does the same thing, but changes the `$last-turn` value based on if it is `$p2` or not, but then passes the input to an _iterative_ solution. The iterative solution basically just keeps the last-said number in memory and checks if it exists in our `%number` `Hash`. If so, it finds the difference between the last turn, and the last time it was said and that is our next number, otherwise it is `0`. We then add that new number to `%numbers` and keep going.

For 30 million iterations this solution is still pretty slow, but it works where the recursive solution just dies.

##### Specific Comments

1. The `is copy` parameter tells the subroutine that it is receiving a `copy` of `%numbers` and it is safe to mutate it.
2. Since a `Hash` does not guarantee order, we need to implement a custom sort algorithm. In this case, we are sorting by the `value` of the `Pair` objects, which is the `turn` in our scenario. The `$^a` syntax is special here in that it assigns and uses a variable all at once. This is the equivalent of `.sort(-> $a, $b { $a.value cmp $b.value })`.
3. The `^..` syntax means it is a range _exclusive_ of the bottom end but _inclusive_ of the top; the corresponding math notation is `(a, b]`.
4. Raku (like many languages) allows us to put underscores in numeric literals to make them easier to read.

## Final Thoughts

This is obviously a time when recursion is not the best idea. It's important to be able to distinguish what can be done recursively and what must be done iteratively, even if the recursive solution seems more "natural."
