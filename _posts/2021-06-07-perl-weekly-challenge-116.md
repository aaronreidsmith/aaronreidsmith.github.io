---
title: "Perl Weekly Challenge 116"
categories:
  - Blog
tags:
  - Perl Weekly Challenge
  - Raku
---

Part 1 was probably the hardest this week, but I ended up being able to adapt a solution from an existing Python library. 

## Task 1: Number Sequence

You are given a number `$N >= 10`.

Write a script to split the given number such that the difference between two consecutive numbers is always 1 and it shouldn’t have leading 0.

Print the given number if it's impossible to split the number.

### Examples

```
Input: $N = 1234
Output: 1,2,3,4

Input: $N = 91011
Output: 9,10,11

Input: $N = 10203
Output: 10203 as it is impossible to split satisfying the conditions.
```

### Solution

[GitHub Link](https://github.com/manwar/perlweeklychallenge-club/blob/master/challenge-116/aaronreidsmith/raku/ch-1.raku)

See below for explanation and any implementation-specific comments.

```
# Raku adaptation of Python's more-itertools.partitions: https://git.io/JZL8Q
sub partitions(Str $S) {
  my @sequence = $S.comb;
  my $n = @sequence.elems;
  my @partitions = gather for (1..^$n).combinations -> @combination {
    my @partition = gather for (0, |@combination) Z (|@combination, $n) -> ($i, $j) {
      take [@sequence[$i..^$j]];
    }
    take @partition;
  }
  gather for @partitions -> @partition {
    # Filter out elements with leading zeros
    my @invalid = @partition.grep(*.head eq '0');
    if @invalid.elems == 0 {
      take @partition.map(*.join.Int);
    }
  }
}

sub challenge(Int $N where $N >= 10) returns Str {
  my $S = $N.Str;
  my $solution = partitions($S).first: -> @partition {         # [1]
    my @zipped = @partition[0..*-1] Z @partition[1..*];        # [2]
    my @filtered = @zipped.grep(-> ($a, $b) { $b - $a == 1 }); # [3]
    @zipped.elems > 0 && @zipped.elems == @filtered.elems;     # [4]
  }

  with $solution { # [5]
    $solution.join(',');
  } else {
    $S
  }
}

sub MAIN(Int $N) {
  say challenge($N);
}
```

This program runs as such:

```
$ raku ch-1.raku 1234
1,2,3,4
```

### Explanation

I won't focus on the `partitions` function too much, as it is just a means to and end. At a high level, it takes a string (let's say `1234`) and returns a list that looks like this: `((1234) (1 234) (12 34) (123 4) (1 2 34) (1 23 4) (12 3 4) (1 2 3 4))`; basically every permutation of every size split possible (with order maintained). Once we have that list of partitions, we want to find the first one that satisfies our condition -- each element is 1 less than the next element. If we found one, return it as a comma-separated string. Otherwise, return the input.

#### Specific comments

1. `first` is kind of like `collectFirst` in Scala; it will return either the element that matches the condition or `Nil` if nothing matches.
2. To compare our elements pairwise, we need to zip them up like so. In Scala this could be `partition.init.zip(partition.tail)` or `partition.sliding(2)`, but again, Raku doesn't have those cool functions.
3. Now that we have the zipped up, we filter it to down to elements that match our condition.
4. Finally, if `@filtered` didn't remove anything, then this is a winner! We also need to check if `@zipped` is non-empty, because a `@partition` of size 1 will cause that.
5. `with` is the same as saying `if $solution.defined`, since `$solution` can be `Nil`.
  
## Task 2: Sum of Squares

You are given a number `$N >= 10`.

Write a script to find out if the given number `$N` is such that sum of squares of all digits is a perfect square. Print 1 if it is otherwise 0.

### Examples

```
Input: $N = 34
Ouput: 1 as 3^2 + 4^2 => 9 + 16 => 25 => 5^2

Input: $N = 50
Output: 1 as 5^2 + 0^2 => 25 + 0 => 25 => 5^2

Input: $N = 52
Output: 0 as 5^2 + 2^2 => 25 + 4 => 29
```

### Solution

[GitHub Link](https://github.com/manwar/perlweeklychallenge-club/blob/master/challenge-116/aaronreidsmith/raku/ch-2.raku)

See below for explanation and any implementation-specific comments.

```
sub challenge(Int $N where $N >= 10) returns Int {
  my $square-sum = $N.comb.map(*²).sum;     # [1][2]
  $square-sum.sqrt.narrow ~~ Int ?? 1 !! 0; # [3]
}

sub MAIN(Int $N) {
  say challenge($N);
}
```

This program runs as such:

```
$ raku ch-2.raku 34
1
```

### Explanation

We convert the input number to a list of digits, then square each digit, then sum all the squares. We then check if the sum of squares is an integer (i.e., a perfect square). If so, we return `1`, else `0`.

#### Specific Comments

1. I like the first part support of Unicode in Raku. It makes it very clear we are squaring each element of a list.
2. I don't like this -- this takes 2 passes (one for squaring and one for summing). In Scala, I would write `list.foldLeft(0)((runningSum, elem) => runningSum + math.pow(elem, 2))`, which only takes one pass. However, the `math.pow` is uglier than it is in Raku, so you win some you lose some.
3. `narrow` returns the most granular numerical type that this number matches (`sqrt` returns a `Numeric`). If it is an `Int`, this is a perfect square.

## Final Thoughts

Two fun challenges this week! Glad I am ahead of the curve and won't be behind due to a busy weekend this week.
