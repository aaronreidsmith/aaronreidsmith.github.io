---
title: "Perl Weekly Challenge 91"
categories:
  - Blog
tags:
  - Perl Weekly Challenge
  - Raku
---

I finally got some time between my day job and Advent of Code to tackle this week's Perl Weekly Challenge. Pretty easy stuff this week; hope the difficulty ramps up soon!

## Task 1: Count Number

You are given a positive number `$N`.

Write a script to count number and display as you read it.

### Example 1

```
Input: $N = 1122234  # ("two 1 three 2 one 3 one 4")
Output: 21321314
```

### Example 2

```
Input: $N = 2333445  # ("one 2 three 3 two 4 one 5")
Output: 12332415
```

### Example 3

```
Input: $N = 12345  # ("one 1 one 2 one 3 one 4 one 5")
Output: 1112131415
```

### Solution

[GitHub Link](https://github.com/manwar/perlweeklychallenge-club/blob/master/challenge-091/aaronreidsmith/raku/ch-1.raku)

See below for explanation and any implementation-specific comments.

```
sub challenge($N) {
    my @digits = $N.comb.map(*.Int);

    my ($current-num, $current-count);
    my $first = True;
    my @output;
    for @digits.kv -> $index, $digit {
        # If this is the first round, just set our variables and continue
        if $first {
            $first = False;
            $current-num = $digit;
            $current-count = 1;
            next;
        }

        # Otherwise, just keep track of our current digit/count
        if $digit == $current-num {
            $current-count += 1;
        } else {
            @output.push($current-count);
            @output.push($current-num);
            $current-num = $digit;
            $current-count = 1;
        }

        # We need this to push the last number on, or it will get lost
        if $index == @digits.elems - 1 {
            @output.push($current-count);
            @output.push($current-num);
        }
    }

    @output.join;
}

multi sub MAIN($N where $N ~~ Int && $N > 0) {
    say challenge($N);
}

multi sub MAIN(:$test) {
    use Test;

    my @tests = (
        (1122234, 21321314),
        (2333445, 12332415),
        (12345, 1112131415)
    );

    for @tests -> @test {
        is(challenge(@test[0]), @test[1]);
    }

    done-testing;
}
```

This program runs as such:

```
$ raku ch-1.raku 1122234
21321314

$ raku ch-1.raku --test
ok 1 - 
ok 2 - 
ok 3 - 
1..3
```

### Explanation

You can see this week I started adding tests for my scripts (utilized by passing in the `--test` flag), so all the logic lives in `challenge`.

The logic is pretty easy --  as we iterate from left-to-right we keep track of the current digit and its count. If we encounter a new digit, we push the old `$current-digit` and old `$current-count` onto `@output` and reset our variables. The only special handling is around the first digit (when there is no `$current-digit`), and the last digit (since we need to store the last digit and count before exiting).
  
## Task 2: Jump Game

You are given an array of positive numbers `@N`, where value at each index determines how far you are allowed to jump further.

Write a script to decide if you can jump to the last index. Print 1 if you are able to reach the last index otherwise 0.

### Solution

[GitHub Link](https://github.com/manwar/perlweeklychallenge-club/blob/master/challenge-091/aaronreidsmith/raku/ch-2.raku)

See below for explanation and any implementation-specific comments.

```
subset PositiveInt of Int where { $_ >= 0 }

sub challenge(@N) {
    my Int $pointer = 0;
    my Bool $reached-the-end;

    loop {
        given $pointer {
            when * < @N.elems - 1  {
                my $value = @N[$pointer];
                if $value == 0 {
                    $reached-the-end = False;
                    last;
                } else {
                    $pointer += @N[$pointer]
                }
            }
            when * == @N.elems - 1 {
                $reached-the-end = True;
                last;
            }
            when * > @N.elems - 1  {
                $reached-the-end = False;
                last;
            }
        }
    }

    $reached-the-end.Int;
}

multi sub MAIN(*@N where all(@N) ~~ PositiveInt) {
    say challenge(@N);
}

multi sub MAIN(:$test) {
    use Test;

    my @tests = (
        ((1, 2, 1, 2), 1),
        ((2, 1, 1, 0, 2), 0)
    );

    for @tests -> @test {
        is(challenge(@test[0]), @test[1]);
    }

    done-testing;
}

```

This program runs as such:

```
$ raku ch-2.raku 1 2 1 2
1

$ raku ch-2.raku --test
ok 1 - 
ok 2 - 
1..2
```

### Explanation

We set the `$pointer` to start at index 0 and enter an infinite loop. If we are not at the end we have to check if the current value is `0`. If it _is_, we have gone as far as we can and need to exit (`last`), otherwise keep going. If we are _at_ at the end, exit and mark` $reached-the-end` as `True`. If we have passed the end, exit and mark `$reached-the-end` as `False`. Since the problem asks for an integer output, we have to cast our boolean to an integer before returning.

## Final Thoughts

Nothing ground breaking this week. However, we did get to explore one of the cooler features of Raku for Advent of Code day 18. [Give it a read](https://aaronreidsmith.github.io/blog/advent-of-code-day-18/)!