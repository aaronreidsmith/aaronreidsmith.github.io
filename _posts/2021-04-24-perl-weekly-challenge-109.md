---
title: "Perl Weekly Challenge 109"
categories:
  - Blog
tags:
  - Perl Weekly Challenge
  - Raku
---

Two fun tasks this week that were both able to be solved in a functional manner 🎉

## Task 1: Chowla Numbers

Write a script to generate first 20 `Chowla Numbers`, named after, **Sarvadaman D. S. Chowla**, a London born Indian American mathematician. It is defined as:

```
C(n) = sum of divisors of n except 1 and n
```

### Output

```
0, 0, 0, 2, 0, 5, 0, 6, 3, 7, 0, 15, 0, 9, 8, 14, 0, 20, 0, 21
```

### Solution

[GitHub Link](https://github.com/manwar/perlweeklychallenge-club/blob/master/challenge-109/aaronreidsmith/raku/ch-1.raku)

See below for explanation and any implementation-specific comments.

```
sub challenge(Int $n) returns Int {
    (2..$n / 2).grep($n %% *).sum; # [1][2]
}

sub MAIN(Int $terms = 20) {
    say (1..$terms).map(&challenge).join(', '); # [3]
}
```

This program runs as such:

```
$ raku ch-1.raku
0, 0, 0, 2, 0, 5, 0, 6, 3, 7, 0, 15, 0, 9, 8, 14, 0, 20, 0, 21
```

### Explanation

Basically we find all the factors of `$n` excluding (`1` and `$n`), then just sum them. We do this for the range `1..$terms` (in this case 20) and join them all with a comma to match the provided output.

#### Specific comments

1. To find the factors of a given number, we only have to look at numbers from `1` to `$n / 2` and `$n` itself. Since `1` and `$n` are excluded from Chowla numbers by definition, we just go from `2` to `$n / 2`.
2. `grep` is Raku's version of `filter`. Additionally, Raku has a built-in operator for "is divisible by" (`%%`). Finally, we are able to use the "whatever star" since this is such a simple anonymous function. So basically, for each potential factor, we check if `$n` is divisible by that number.
3. Since the challenge operates on each number individually (rather than all 20 at once), we map the function over each number and join the output with a comma.
  
## Task 2: Four Squares Puzzle

You are given four squares as below with numbers named a, b, c, d, e, f, g.

```
              (1)                    (3)
        ╔══════════════╗      ╔══════════════╗
        ║              ║      ║              ║
        ║      a       ║      ║      e       ║
        ║              ║ (2)  ║              ║  (4)
        ║          ┌───╫──────╫───┐      ┌───╫─────────┐
        ║          │   ║      ║   │      │   ║         │
        ║          │ b ║      ║ d │      │ f ║         │
        ║          │   ║      ║   │      │   ║         │
        ║          │   ║      ║   │      │   ║         │
        ╚══════════╪═══╝      ╚═══╪══════╪═══╝         │
                   │       c      │      │      g      │
                   │              │      │             │
                   │              │      │             │
                   └──────────────┘      └─────────────┘
```

Write a script to place the given unique numbers in the square box so that sum of numbers in each box is the same.

### Example

```
Input: 1,2,3,4,5,6,7

Output:

    a = 6
    b = 4
    c = 1
    d = 5
    e = 2
    f = 3
    g = 7

    Box 1: a + b = 6 + 4 = 10
    Box 2: b + c + d = 4 + 1 + 5 = 10
    Box 3: d + e + f = 5 + 2 + 3 = 10
    Box 4: f + g = 3 + 7 = 10
```

### Solution

[GitHub Link](https://github.com/manwar/perlweeklychallenge-club/blob/master/challenge-109/aaronreidsmith/raku/ch-2.raku)

See below for explanation and any implementation-specific comments.

```
sub challenge(@nums where @nums.elems == 7) returns Str {
  my @solution = @nums
    .sort                                     # [1]
    .permutations                             # [2]
    .reverse                                  # [3]
    .first: -> ($a, $b, $c, $d, $e, $f, $g) { # [4][5]
      $a + $b == $b + $c + $d &&
      $b + $c + $d == $d + $e + $f &&
      $d + $e + $f == $f + $g
    };

  if @solution.elems == 1 {                       # [6]
    "Unable to find a solution for given input.";
  } else {
    (<a b c d e f g> Z @solution)                 # [7][8]
      .map(-> ($key, $value) { "$key = $value" }) # [9]
      .join("\n");
  }
}

sub MAIN(*@nums where all(@nums) ~~ Int) {
  say challenge(@nums);
}
```

This program runs as such:

```
$ raku ch-2.raku 1 2 3 4 5 6 7
a = 7
b = 3
c = 2
d = 5
e = 1
f = 4
g = 6
```

### Explanation

Raku helps us out quite a bit here with its `permutations` function. Basically, the actual squares are irrelevant and all we need to check is:

```
$a + $b == $b + $c + $d &&
$b + $c + $d == $d + $e + $f &&
$d + $e + $f == $f + $g
```

So we just go through each permutation of the 7 numbers we are given (5040 permutations, so should be quick) and find the first instance where the above condition is true.

You'll also notice our output is different from the example output. That is because the following pairs are interchangeable:

- `$a` and `$g`
- `$b` and `$f`
- `$c` and `$e`

Since we maximize `$a`, our output is different, but still correct.

#### Specific Comments

1. `$a` and `$g` have to be comparatively big numbers compared to the rest, so we sort our input (and later reverse it) and start checking those permutations first.
2. Raku will automatically generate all permutations of a list with this function. It only works with <20 terms, which is perfect for this use case.
3. As I said in (1), we are reversing our list of permutations to start with the ones where `$a` is greatest.
4. I have decided to start using the `first: -> {}` syntax for multi-line anonymous functions rather than the `first(->  {})` syntax, as I feel the trailing parenthesis looks out of place.
5. Raku allows us to unpack our individual permutation into variables, so `$a` through `$g` are all assigned in this one line.
6. `first` returns `Nil` if it can't find a match. _However_, assigning `Nil` to a positional variable (denoted by the `@` sigil) will generate a list that looks like this `[(Any)]`, so we check for size equal to 1 rather than checking if it is `Nil`.
7. To get our numbers assigned to their letters, we need to zip them with the sequence `a` through `g`. The output of this is a list that looks like this `((a 7) (b 3) (c 2) (d 5) (e 1) (f 4) (g 6))`.
8. The `<>` syntax allows us to make a list of space-separated terms. It also makes each term a string automagically; it is basically shorthand for `('a', 'b', 'c', 'd', 'e', 'f', 'g')`.
9. When we map over this list of pairs, we unpack each pair into its `$key` and `$value` and turn that into a string of `$key = $value`. We then join this list of strings using newlines to match the provided output.

## Final Thoughts

I'm always happy when I can find a functional solution to these problems, so I had fun this week. 🙂 See y'all next week!
