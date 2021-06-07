---
title: "Perl Weekly Challenge 115"
categories:
  - Blog
tags:
  - Perl Weekly Challenge
  - Raku
---

I had a very busy weekend and didn't get the opportunity to post this during the actual week of the challenge, but I will post both 115 and 116 today!

## Task 1: String Chain

You are given an array of strings.

Write a script to find out if the given strings can be chained to form a circle. Print 1 if found otherwise 0.

> A string $S can be put before another string $T in circle if the last character of $S is same as first character of $T.

### Examples

```
Input: @S = ("abc", "dea", "cd")
Output: 1 as we can form circle e.g. "abc", "cd", "dea".

Input: @S = ("ade", "cbd", "fgh")
Output: 0 as we can't form circle.
```

### Solution

[GitHub Link](https://github.com/manwar/perlweeklychallenge-club/blob/master/challenge-115/aaronreidsmith/raku/ch-1.raku)

See below for explanation and any implementation-specific comments.

```
sub challenge(@S) returns Int {
  my @solutions = @S.race.permutations.grep: -> @permutation { # [1][2]
    my $valid = True;
    for @permutation Z (|@permutation[1..*], @permutation.head) -> ($a, $b) { # [3]
      if $a.comb.tail ne $b.comb.head {
        $valid = False;
        last;
      }
    }
    $valid;
  }
  (@solutions.elems > 0).Int;
}

sub MAIN(*@S where all(@S) ~~ Str) {
  say challenge(@S);
}
```

This program runs as such:

```
$ raku ch-1.raku abc dea cd
1
```

### Explanation

For this problem, we start by finding all the permutations of our input. So for `("abc", "dea", "cd")` we would get `((abc dea cd) (abc cd dea) (dea abc cd) (dea cd abc) (cd abc dea) (cd dea abc))`. We then take each one individually and compare each element pairwise. Since the last element needs to be compared to the first element, we have the special zip discussed in #3 below. If the last element of each string matches the first element of the next string, then we have a valid chain; otherwise, we exit early. Finally, we convert the boolean `@solutions.elems > 0` to an integer to match the problem.

#### Specific comments

1. We can process each permutation separately and order does not matter, so we convert our input to a `RaceSeq` as early as possible.
2. `permutations` only works for positionals with size < 20, or else it will blow up the stack.
3. If we have the list `(a, b, c)` here, what we are trying to generate is `((a, b), (b, c), (c, a))`. In Scala, this could be written as `(list :+ list.head).sliding(2)`, but Raku doesn't have that functionality, so this line does the same thing by creating a second list with the first element moved to the end, _and then_ zipping.
  
## Task 2: Largest Multiple

You are given a list of positive integers (0-9), single digit.

Write a script to find the largest multiple of 2 that can be formed from the list.

### Examples

```
Input: @N = (1, 0, 2, 6)
Output: 6210

Input: @N = (1, 4, 2, 8)
Output: 8412

Input: @N = (4, 1, 7, 6)
Output: 7614
```

### Solution

[GitHub Link](https://github.com/manwar/perlweeklychallenge-club/blob/master/challenge-115/aaronreidsmith/raku/ch-2.raku)

See below for explanation and any implementation-specific comments.

```
sub challenge(@N) returns Int {
  @N.race.permutations.map(*.join.Int).grep(* %% 2).max; # [1]
}

sub MAIN(*@N where all(@N) ~~ /^<digit>$/) { # [2]
  say challenge(@N);
}
```

This program runs as such:

```
$ raku ch-2.raku 1 0 2 6
6210
```

### Explanation

Once again, we find all the permutations and then map all of them to integers. We then filter them to only numbers divisible by 2, and then find the max. Easy peasy!

#### Specific Comments

1. Raku has a cool built-in operator for "divisible by" which comes in handy in these situations.
2. The question says to only accept positive integers between 0 and 9, in other words, a digit, so we enforce that at runtime using this regex.

## Final Thoughts

Permutations and `RaceSeq` make for fairly efficient and readable solutions this week! See y'all in Challenge 116.
