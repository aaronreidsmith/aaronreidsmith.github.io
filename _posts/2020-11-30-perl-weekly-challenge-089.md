---
title: "Perl Weekly Challenge 89"
last_modified_at: 2020-12-01T08:40:30-05:00
categories:
  - Blog
tags:
  - Perl Weekly Challenge
  - Raku
---

Back again with challenge 89! I was able to tackle this one the day it was released, but I doubt that will be the case going forward.

Once again, it seems the first task can be tackled easily in a functional way and the second one ends up being more imperative. Hoping I can try to do more things functionally in the future!

## Task 1: GCD Sum

You are given a positive integer `$N`.

Write a script to sum [GCD](https://en.wikipedia.org/wiki/Greatest_common_divisor) of all possible unique pairs between 1 and `$N`.

### Example 1

```
Input: 3
Output: 3

gcd(1,2) + gcd(1,3) + gcd(2,3)
```

### Example 2

```
Input: 4
Output: 7

gcd(1,2) + gcd(1,3) + gcd(1,4) + gcd(2,3) + gcd(2,4) + gcd(3,4)
```

### Solution

[GitHub Link](https://github.com/manwar/perlweeklychallenge-club/blob/master/challenge-089/aaronreidsmith/raku/ch-1.raku)

See below for explanation and any specific implementation comments.

```
sub MAIN($N where $N ~~ Int && $N > 0) {
    my @pairs = (1..$N).combinations(2);                    # [1]
    say [+] @pairs.map(-> @pair { @pair[0] gcd @pair[1] }); # [2][3]
}
```

This program runs as such:

```
$ raku ch-1.raku 3
3

$ raku ch-1.raku 4
7
```

### Explanation

The thought process here is pretty straight forward:

1. Find all pairs from 1 to `$N`
2. Find the GCD of each pair
3. Sum the GCDs produced in step 2

You'll see my functional programming background bubbling up again. In fact, this could honestly be a one-liner if I weren't going for readability:

```
say [+] (1..$N).combinations(2).map(-> @pair { @pair[0] gcd @pair[1] });
```

#### Specific comments

1. Raku provided a great subroutine to find all the pairs in a list ([`combinations`](https://docs.raku.org/routine/combinations)). In fact, it is generalized such that you can take more than just pairs (if I didn't provide a number, it would find _all_ combinations from `size=0` to `size=$N`), so it may come back in future problems!
2. This was an interesting one for me. In Scala, since it is so strongly and statically typed, we know that the `@pairs` list contains lists itself, so you could just say: `pairs.map(_._1 gcd _._2)`. In Raku, I had to use the [pointy block](https://docs.raku.org/language/functions#Blocks_and_lambdas) notation to give the mapped items a name and, more importantly, a sigil to treat it as a list. 
3. I _love_ that a lot of simple things (like [`gcd`](https://docs.raku.org/routine/gcd) or [`is-prime`](https://docs.raku.org/routine/is-prime)) are built right into Raku. It saves a lot of boilerplate code and potentially bad implementation of these functions.

  
## Task 2: Magic Matrix

Write a script to display matrix as below with numbers `1 - 9`. Please make sure numbers are used once.

```
[ a b c ]
[ d e f ]
[ g h i ]
```

So that it satisfies the following:

```
a + b + c = 15
d + e + f = 15
g + h + i = 15
a + d + g = 15
b + e + h = 15
c + f + i = 15
a + e + i = 15
c + e + g = 15
```

### Solution

[GitHub Link](https://github.com/manwar/perlweeklychallenge-club/blob/master/challenge-089/aaronreidsmith/raku/ch-2.raku)

See below for explanation and any implementation-specific comments.

```
subset OddPositiveInt of Int where { $_ ~~ Int && $_ > 0 && !($_ %% 2) }

sub MAIN($side-length where $side-length ~~ OddPositiveInt = 3, $debug where $debug ~~ Bool = False) {
    my @matrix = generate-matrix($side-length);
    my @filled-in-matrix = fill-in-matrix(@matrix, $side-length);
    for @filled-in-matrix -> @row {
        say '[ ' ~ @row.join(' ') ~ ' ]';
    }
    if $debug {
        print "\n";
        validate-matrix(@filled-in-matrix, $side-length);
    }
}

# Generate a 2D matrix that we can fill in with the proper numbers.
# For 3x3 it would output:
#  [0 0 0]
#  [0 0 0]
#  [0 0 0]
sub generate-matrix($side-length) {
    my @matrix = Array.new;
    for ^$side-length -> $i {
        my @row = Array.new;
        for (($i * $side-length) + 1..($i * $side-length) + $side-length) {
            @row.push(0);
        }
        @matrix.push(@row);
    }
    @matrix
}

# Actual business logic here. It takes the empty array and fills it in to be "magic"
# Such that all rows, columns, and the two diagonals add up to $side-length * ($side-length² + 1) / 2
sub fill-in-matrix(@matrix, $side-length) {
    my $num = 1;
    my $row = floor($side-length / 2);
    my $col = $side-length - 1;

    while $num <= $side-length² {                # [1]
        if $row == -1 && $col == $side-length {  # Condition 3 (see below)
            $col = $side-length - 2;
            $row = 0;
        } else {
            if $col == $side-length {            # Condition 1 (see below)
                $col = 0;
            }
            if $row < 0 {
                $row = $side-length - 1;
            }
        }
        if @matrix[$row][$col] != 0 {           # Condition 2 (see below)
            $col -= 2;
            $row++;
        } else {
            @matrix[$row][$col] = $num;
            $num++;
            $col++;
            $row--;
        }
    }
    @matrix;
}

# Helper function to validate output matrix and print the validation
sub validate-matrix(@matrix, $side-length) {
    my @rows = @matrix;
    my @columns = [Z] @matrix;                                                   # [2]
    my @diagonal = @matrix.kv.map(-> $i, @row { @row[$i] });
    my @counter-diagonal = @matrix.kv.map(-> $i, @row { @row[*-$i-1] });

    my $target = ($side-length * ($side-length² + 1) / 2).Int;

    my $valid-rows = so @rows.map(-> @row { [+] @row }).all == $target;          # [3]
    my $valid-cols = so @columns.map(-> @column { [+] @column }).all == $target;
    my $valid-diag = so ([+] @diagonal) == $target;
    my $valid-counter-diag = so ([+] @counter-diagonal) == $target;

    if $valid-rows && $valid-cols && $valid-diag && $valid-counter-diag {
        for @rows -> @row {
            say @row.join(' + ') ~ ' = ' ~ $target;
        }
        for @columns -> @column {
            say @column.join(' + ') ~ ' = ' ~ $target;
        }
        say @diagonal.join(' + ') ~ ' = ' ~ $target;
        say @counter-diagonal.join(' + ') ~ ' = ' ~ $target;
    } else {
        die "Not a valid magic matrix";
    }
}
```

This program runs as such:

```
$ raku ch-2.raku
[ 2 7 6 ]
[ 9 5 1 ]
[ 4 3 8 ]

# There is an optional `debug` parameter that can be supplied, but the `side-length` argument must also be provided
$ raku ch-2.raku 3 True
[ 2 7 6 ]
[ 9 5 1 ]
[ 4 3 8 ]

2 + 7 + 6 = 15
9 + 5 + 1 = 15
4 + 3 + 8 = 15
2 + 9 + 4 = 15
7 + 5 + 3 = 15
6 + 1 + 8 = 15
2 + 5 + 8 = 15
6 + 5 + 4 = 15
```

It should be noted this program only works with odd side-length squares


### Explanation

Full disclosure, I have done this problem before, so I basically just ported some old code. There are two steps to this problem before we even get to implementation:

1. Find the pattern for what the sum is
  - As seen in the code, you will find it is `N(N²+1)/2`
2. Draw some "magic matrices" to see if you can find any patterns

You will find 3 patterns hold true (I am copying these from [Geeks for Geeks](https://www.geeksforgeeks.org/magic-square/)):

1. The position of next number is calculated by decrementing row number of the previous number by 1, and incrementing the column number of the previous number by 1. At any time, if the calculated row position becomes -1, it will wrap around to n-1. Similarly, if the calculated column position becomes n, it will wrap around to 0.
2. If the magic square already contains a number at the calculated position, calculated column position will be decremented by 2, and calculated row position will be incremented by 1.
3. If the calculated row position is -1 & calculated column position is n, the new position would be: (0, n-2).

Basically, we just start in the middle right square and apply the above criteria iteratively and it works for any odd-side-lengthed square.

#### Specific comments

1. Raku supports Unicode, so you'll notice I used `$side-length²` rather than `$side-length ** 2`. It's a small feature that I find helps readibilty (but can be hard to write)!
2. This has been called out as a [trick to avoid](https://docs.raku.org/language/traps#Using_[%E2%80%A6]_metaoperator_with_a_list_of_lists) because it fails when you get a matrix with 1 row. Since it is being used in a debugging function and if we _did_ get a 1-row matrix it would be 1x1, so I think it is safe to use here
3. I don't really like that `so` is the subroutine used to cast input to a boolean, so I just wanted to call out that (a) that is what these lines are doing and (b) I don't like the terminology.


## Final Thoughts

I'm really glad I decided to start doing these challenges weekly, and I may even go back and attempt old challenges if I have time.

With that being said, I am kind of disappointed in myself for just copying old code for task two. For one, I have grown as a programmer since writing that, and two, it seems past-me just copied that code from somewhere on the internet. While it was kind of challenging porting it to Raku, I feel like it was the lazy way out. 
