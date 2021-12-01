---
title: "Perl Weekly Challenge 92"
categories:
  - Blog
tags:
  - Perl Weekly Challenge
  - Raku
---

It was a slow Christmas day for me, for the most part, so I decided to knock this challenge out as well as [finishing up AoC](https://aaronreidsmith.github.io/blog/advent-of-code-year-2020-day-25/)!

## Task 1: Isomorphic Strings

You are given two strings `$A` and `$B`.

Write a script to check if the given strings are [isomorphic](https://www.educative.io/edpresso/how-to-check-if-two-strings-are-isomorphic). Print `1` if they are otherwise `0`.

### Example 1

```
Input: $A = "abc"; $B = "xyz"
Output: 1
```

### Example 2

```
Input: $A = "abb"; $B = "xyy"
Output: 1
```

### Example 3

```
Input: $A = "sum"; $B = "add"
Output: 0
```

### Solution

[GitHub Link](https://github.com/manwar/perlweeklychallenge-club/blob/master/challenge-092/aaronreidsmith/raku/ch-1.raku)

See below for explanation and any implementation-specific comments.

```
use MONKEY-TYPING;  # [1]

augment class Seq {
    method OrderedSet {
        my @set;
        for self -> $item {
            next if $item ∈ @set;
            @set.push($item);
        }
        @set;
    }
}

sub challenge(Str $A, Str $B) returns Int {
    my $a-chars = $A.comb.OrderedSet.join;
    my $b-chars = $B.comb.OrderedSet.join;
    ($A.trans($a-chars => $b-chars) eq $B).Int;
}

multi sub MAIN(Str $A, Str $B) {
    say challenge($A, $B);
}

multi sub MAIN(Bool :$test) {
    use Test;

    my @tests = (
        ('abc', 'xyz', 1),
        ('abb', 'xyy', 1),
        ('sum', 'add', 0)
    );

    for @tests -> @test {
        is(challenge(@test[0], @test[1]), @test[2]);
    }

    done-testing;
}
```

This program runs as such:

```
$ raku ch-1.raku abc xyz
1

$ raku ch-1.raku --test
ok 1 - 
ok 2 - 
ok 3 - 
1..3
```

### Explanation

Once again, most the logic lives in `challenge`. Basically, I wanted to take advantage of something we used [a couple weeks ago](https://aaronreidsmith.github.io/blog/perl-weekly-challenge-090), the `trans` subroutine. `trans` takes two strings and _translates_ the given input using the map. If I were to hardcode it for the example, this is basically what I am trying to check:

```
'abc'.trans('abc' => 'xyz') eq 'xyz'
```

To do this we need to remove duplicates (so we need a `Set`), but we also need to preserve order (so something like an `OrderedSet`). Unfortunately, such a thing doesn't exist in Raku... so we have to create it!

I am doing something which is _technically_ [frowned upon](https://docs.raku.org/syntax/augment) by using the `augment` keyword, but it is a fairly normal pattern in Scala, so I just went with it. Basically, we just [monkey patch](https://en.wikipedia.org/wiki/Monkey_patch) an `OrderedSet` method onto the existing `Seq` builtin. In Scala, we would do this via an implicit class; here is an example:

```scala
implicit class ExtendedString(str: String) {
	def excited: String = s"$str!!!"
}

"Hello world".excited
// Hello world!!!
```

I feel Raku makes this much clearer via the `augment` keyword. It says we are _augmenting_ the class `Seq` and then we define the `OrderedSet` method. The method itself does not _technically_ return a `Set`, but it returns a `List` that maintains order and removes duplicates -- all we need.

Once we have both the left and right strings converted to ordered sets, we convert them _back_ into strings to use in the `trans` method as shown above

#### Specific Comments

1. If we want to use the "frowned upon" pragma of monkey patching, we have to manually turn it on using `use MONKEY-TYPING`.
  
## Task 2: Insert Interval

You are given a set of sorted non-overlapping intervals and a new interval.

Write a script to merge the new interval to the given set of intervals.

### Example 1

```
Input $S = (1,4), (8,10); $N = (2,6)
Output: (1,6), (8,10)
```

### Example 2

```
Input $S = (1,2), (3,7), (8,10); $N = (5,8)
Output: (1,2), (3,10)
```

### Example 3

```
Input $S = (1,5), (7,9); $N = (10,11)
Output: (1,5), (7,9), (10,11)
```

### Solution

[GitHub Link](https://github.com/manwar/perlweeklychallenge-club/blob/master/challenge-092/aaronreidsmith/raku/ch-2.raku)

See below for explanation and any implementation-specific comments.

```
subset MultiRange of Str where { $_ ~~ /^[<digit>+'-'<digit>+',']+[<digit>+'-'<digit>+]$/ }
subset Range of Str where { $_ ~~ /^<digit>+'-'<digit>+$/ }

sub challenge(@S, $N) {
    my @combined = (|@S, $N).sort({ $^a.min cmp $^b.min });
    my @final = (@combined.head,);
    OUT: for @combined[1..*] -> $new-range {           # [1]
        my ($min, $max) = $new-range.minmax;
        IN: for @final.kv -> $index, $range {
            next IN if $min ∈ $range && $max ∈ $range; # [2]
            if $min ∈ $range {
                @final[$index] = ($range.min..$max);
                next OUT;
            } elsif $max ∈ $range {
                @final[$index] = ($min..$range.max);
                next OUT;
            } elsif $index == @final.end {
                @final.push($new-range);
            }
        }
    }
    @final.map(-> $range { "({$range.min},{$range.max})" }).join(', ');
}

multi sub MAIN(MultiRange :$S, Range :$N) {
    my @s = $S.split(',').map(*.split('-').map(*.Int).minmax);
    my $n = $N.split('-').map(*.Int).minmax;
    say challenge(@s, $n);
}

multi sub MAIN(Bool :$test) {
    use Test;

    my @tests = (
        ((1..4), (8..10), (2..6), '(1,6), (8,10)'),
        ((1..2), (3..7), (8..10), (5..8), '(1,2), (3,10)'),
        ((1..5), (7..9), (10..11), '(1,5), (7,9), (10,11)')
    );

    for @tests -> @test {
        my @S = @test[0..^*-2];
        my $N = @test[*-2];
        my $answer = @test[*-1];
        is(challenge(@S, $N), $answer);
    }

    done-testing;
}
```

This program runs as such:

```
$ raku ch-2.raku -S=1-4,8-10 -N=2-6
(1,6), (8,10)

$ raku ch-2.raku --test
ok 1 - 
ok 2 - 
ok 3 - 
1..3
```

### Explanation

`MAIN` has a little validation and parsing. It validates that `S` contains _at least_ two ranges (defined as `X-Y`) via the `MultiRange` subset, and that we get exactly one range in `N` (via the `Range` subset). It then parses those ranges into actual [`Range`](https://docs.raku.org/type/Range) objects to give to the `challenge` subroutine.

`challenge` first puts all the ranges in order _by their minimum element_ and creates an output list called `@final` that contains the minimum range of the input ranges. We then iterate through the remaining ranges. For each one, we check the following conditions:

1. If it is _wholly contained_ by an existing range, skip it.
2. If the _minimum_ item in our new range is contained in any existing range, extend the existing range up to the new maximum.
3. If the _maximum_ item in our new range is contained in any existing range, extend the existing range down to the new minimum.
4. If we have exhausted all the overlap checks, this must be a totally distinct range and just add it to the end.

Finally, once we have our ranges, we need to convert them to the output format defined, so we do that and return.

#### Specific Comments

1. This is a Raku feature called [Labels](https://docs.raku.org/type/Label), where we can add a label to our [Supply](https://docs.raku.org/type/Supply) objects (`for`, `do`, `gather`, etc). It allows us to name our loops and use the features outline in #2.
2. With labels in place, if we want to break both an inner and an outer loop, we can do that in one statement (`last OUT`), or if we want to go to the next outer loop without finishing our inner loop, we can do that as well (`next OUT`). This makes the code faster and more readable, in my opinion.

## Final Thoughts

Some fun little challenges that nicely complement Advent of Code. Now to start enjoying Christmas with my family! Merry Christmas everyone!