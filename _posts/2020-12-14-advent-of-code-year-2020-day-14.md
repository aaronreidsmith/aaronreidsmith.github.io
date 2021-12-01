---
title: "Advent of Code: Year 2020, Day 14"
categories:
  - Blog
tags:
  - Advent of Code
  - Raku
---

Today was much less math-heavy than yesterday, although we will dive into an algorithm that would make it faster. However, I did do this problem more imperatively than functionally; read on to see why!

## The Problem

### Part 1

As we approach the mainland, the captain once again asks for our help; our computer system is not compatible with the port's docking software. We quickly see that the docking parameters are not being properly initialized. The docking program is using a strange bitmask software, and we don't have the proper chip to decode it. Luckily, we can emulate it.

Our input looks like the following:

```
mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0
```

This defines a 36-bit bitmask and multiple memory addresses to update with bitmasked values. Here is how the bitmask is applied:

```
value:  000000000000000000000000000000001011  (decimal 11)
mask:   XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
result: 000000000000000000000000000001001001  (decimal 73)
```

First, a value (in this case 11) is converted to binary and then the mask is applied by using the mask character if it's a `1` or `0` and the original character if it is an `X`. As you can see, this gives us the number 73 represented as binary. We then store `73` at memory address 8 and move on to the next instruction.

Once all instructions have been applied, what is the sum of values in memory? 

#### Solution

[GitHub Link](https://github.com/aaronreidsmith/advent-of-code/blob/103fedb13cd88b0e852caed8a1ff951d84bffdac/src/main/raku/2020/day-14.raku)

See below for explanation and any implementation-specific comments.

```
sub apply-mask($mask, $num) {
    my @mask-list = $mask.comb;
    my @num-list  = $num.base(2).comb;

    while @num-list.elems < @mask-list.elems {
        @num-list.unshift(0);                                 # [1]
    }

    my @masked = gather {
        for @mask-list Z @num-list -> ($mask-digit, $digit) { # [2]
            take $mask-digit eq 'X' ?? $digit !! $mask-digit;
        }
    }

    @masked.join.parse-base(2);
}

sub extract-values($line) {
    my $address = $line.match(/\[(<digit>+)\]/)[0].Int;
    my $value = $line.split(' = ')[1].Int;
    ($address, $value)
}

sub MAIN($file) {
    my $mask;
    my @mem;
    for $file.IO.lines -> $line {
        if $line.starts-with('mask') {
            $mask = $line.split(' = ')[1];
        } else {
            my ($address, $value) = extract-values($line);
            @mem[$address] = apply-mask($mask, $value);
        }
    }
    say @mem.sum; # [3]
}
```

This runs as such:

```
$ raku day-14.raku input.txt
17934269678453
```

#### Explanation

So, first we define 2 helper functions:

- `apply-mask` takes a `mask` string and an integer, then converts it to binary and iteratively works through the strings to apply the mask to the integer, then it casts the string back to a base-10 integer.
- `extract-values` simply parse the memory address and value to be masked from the input line.

in `MAIN` you can see how imperatively we did this. First, we define a mutable mask<sup>*</sup> and memory register, then start iterating through the lines. If we hit a mask, overwrite our current one, otherwise extract the values, apply the mask, and add it to our memory register. Finally, just sum all the masked values up!

<sup>*</sup>One thing about our input that was not super clear to me in the instructions is that we are given _multiple_ masks that we have to apply to the next N values (until we hit the next mask).

##### Specific Comments

1. `unshift` adds values to the beginning of an array. Raku has no equivalent of Python's [`zip_longest`](https://docs.python.org/3/library/itertools.html#itertools.zip_longest) function, so we have to make sure the input lists are exactly the same length.
2. `Z` is Raku's zip operator. So `(1, 2, 3) Z (4, 5, 6)` yields `((1, 4), (2, 5), (3, 6))`.
3. Notice we never initialized a size of this array. Raku doesn't require us to! It will implicitly fill in any unused slots with `Any`, which is one of its undefined types. `Any` is skipped during the sum, so it really is just as simple as saying `@mem.sum`.

### Part 2

After all that business, we realize the docking computer must be running version 2 of the software while we are still on version 1. 🤦🏻

V2 of the software applies the bitmask to memory _addresses_, not the _values_. Additionally, `X` now means "floating" (`0 or 1`), so we have to update both possible addresses. Here is an example:

```
address: 000000000000000000000000000000101010  (decimal 42)
mask:    000000000000000000000000000000X1001X
result:  000000000000000000000000000000X1101X
```

After the mask, we are left with _four_ addresses to update:

```
000000000000000000000000000000011010  (decimal 26)
000000000000000000000000000000011011  (decimal 27)
000000000000000000000000000000111010  (decimal 58)
000000000000000000000000000000111011  (decimal 59)
```

Using V2, what is the sum of the memory addresses after initialization?

#### Solution

[GitHub Link](https://github.com/aaronreidsmith/advent-of-code/blob/103fedb13cd88b0e852caed8a1ff951d84bffdac/src/main/raku/2020/day-14.raku)

See below for explanation and any implementation-specific comments.

```
sub find-all-masks(@zipped, $pointer = 0, @prefix = ()) {                          # [1]
    if $pointer == @zipped.elems {
        @prefix.join.parse-base(2);
    } else {
        my ($mask-digit, $digit) = @zipped[$pointer];
        given $mask-digit {
            when '0' { find-all-masks(@zipped, $pointer + 1, (|@prefix, $digit)) } # [2]
            when '1' { find-all-masks(@zipped, $pointer + 1, (|@prefix, $mask-digit)) }
            when 'X' {
                |(
                    find-all-masks(@zipped, $pointer + 1, (|@prefix, '0')),
                    find-all-masks(@zipped, $pointer + 1, (|@prefix, '1'))
                )
            }
        }
    }
}

sub apply-mask($mask, $num, Bool $part-two = False) {
    my @mask-list = $mask.comb;
    my @num-list  = $num.base(2).comb;

    while @num-list.elems < @mask-list.elems {
        @num-list.unshift(0);
    }

    if $part-two {
        find-all-masks(@mask-list Z @num-list);
    } else {
        my @masked = gather {
            for @mask-list Z @num-list -> ($mask-digit, $digit) {
                take $mask-digit eq 'X' ?? $digit !! $mask-digit;
            }
        }
        @masked.join.parse-base(2);
    }
}

sub extract-values($line) {
    my $address = $line.match(/\[(<digit>+)\]/)[0].Int;
    my $value = $line.split(' = ')[1].Int;
    ($address, $value)
}

sub MAIN($file, Bool :$p2 = False) {
    my $mask;
    my @mem;
    for $file.IO.lines -> $line {
        if $line.starts-with('mask') {
            $mask = $line.split(' = ')[1];
        } else {
            my ($address, $value) = extract-values($line);
            if $p2 {
                for apply-mask($mask, $address, $p2) -> $index {
                    @mem[$index] = $value;
                }
            } else {
                @mem[$address] = apply-mask($mask, $value);
            }
        }
    }
    say @mem.sum;
}
```

This runs as such:

```
# Part 1
$ raku day-14.raku input.txt
17934269678453

# Part 2
$ raku day-14.raku --p2 input.txt
3440662844064
```

#### Explanation

We made a few tweaks to the original program:

1. If it is `$part-two`, `apply-mask` now returns a list of integers instead of just a single integer.
2. Given the above, if it is `$p2` in `MAIN`, we iterate through the returned list.
3. We added a function `find-all-masks` that will find all binary combinations for the "floating" bits.

The logic is pretty much the same, except using addresses instead of values!

##### Specific Comments

1. This solution works, but it is _slow_ and memory intensive. The correct way to find all of these bit flips is by using something called a [Gray code](https://en.wikipedia.org/wiki/Gray_code).
2. We use these slips all over this to make sure we end up with just a 1D list (per call) when all is said and done.

## Final Thoughts

I am enjoying learning about all the shortcuts that are necessary to make these things run in an acceptable amount of time. Maybe next year I will be able to think of them without writing the brute force solution first!
