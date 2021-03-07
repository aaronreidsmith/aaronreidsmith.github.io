---
title: "Perl Weekly Challenge 102"
categories:
  - Blog
tags:
  - Perl Weekly Challenge
  - Raku
---

Part one was an exercise in efficiency and [short-circuiting](https://en.wikipedia.org/wiki/Short-circuit_evaluation); I am sure there are more optimizations I could add, but it works as is. 🙂 Let me know if you see any obvious ones I could add!

## Task 1: Rare Numbers

You are given a positive integer `$N`.

Write a script to generate all Rare numbers of size `$N` if exists. Please checkout the [page](http://www.shyamsundergupta.com/rare.htm) for more information about it.

**Note:** If you don't want to go to the link above, a rare number basically has the following characteristics:

```
$N + $N.reverse = <perfect square>
$N - $N.reverse = <perfect square>
```

### Examples
```
(a) 2 digits: 65
(b) 6 digits: 621770
(c) 9 digits: 281089082
```

### Solution

[GitHub Link](https://github.com/manwar/perlweeklychallenge-club/blob/master/challenge-102/aaronreidsmith/raku/ch-1.raku)

See below for explanation and any implementation-specific comments.

```
sub digital-root(Int $N) returns Int {
    my @digits = $N.comb;
    my $digital-root = [+] @digits;
    while @digits.elems > 1 {
        @digits = $digital-root.comb;
        $digital-root = [+] @digits;
    }
    $digital-root;
}

sub is-rare(Int $N) returns Bool {
    return False if $N.comb.head % 2 != 0;
    return False if digital-root($N) ~~ 0|1|3|4|6|7; # [1][2]

    my $reversed   = $N.flip.Int;
    my $difference = $N - $reversed;

    if $difference >= 0 && $difference.sqrt.narrow ~~ Int { # [3]
        # Only calculate this if the difference is valid
        my $sum = $N + $reversed;
        $sum.sqrt.narrow ~~ Int;
    } else {
        False;
    }
}

sub challenge(Int $N) returns Str {
    my $min = ('2' ~ ('0' x $N - 1)).Int;
    my $max = ('8' ~ ('9' x $N - 1)).Int;
    ($min..$max).hyper.grep(&is-rare).join(', '); # [4][5]
}

sub MAIN(Int $N) {
    say challenge($N);
}
```

This program runs as such:

```
$ raku ch-1.raku 6
621770
```

### Explanation

This implementation is not overly clever; it basically just goes through every number of size `$N` and checks if it is a rare number. It does use some Raku-isms as well as some logic to short-circuit. For `$N = 6` it runs in ~8 seconds on my machine.

1. Find the minimum and maximum number of size `$N` it _could_ be (according to the link in the challenge, rare numbers cannot start with an odd digit, so for `$N = 6` or range becomes `200000..899999`). 
2. For each candidate:
    - Skip this candidate if the first digit is not even.
    - Skip this candidate if the [digital root](https://en.wikipedia.org/wiki/Digital_root) is not one of 2, 5, 8, or 9 (again, this fact comes from the link in the challenge).
    - Find the reversed number and the difference (only the difference for now. My thought is it is easier to calculate the square root of smaller numbers, so there is no reason to calculate the square root of the larger number if the smaller one fails).
    - If the difference is greater-than-or-equal-to zero _and_ its square root is an integer, calculate the sum and check if it is also a perfect square.
      - If so, return `True`.
      - If any step is false, return `False`.

#### Specific comments

1. Given that my day job is all Scala, where [using `return` is discouraged](https://blog.knoldus.com/scala-best-practices-say-no-to-return/), you'll notice that bleeds into my Raku as well. The reason we use `return` here is to explicitly short-circuit this function in idiomatic Raku (with the condition following the actual declaration [`return False`]).
2. This is an anonymous way to create a [Junction](https://docs.raku.org/type/Junction). In this case, we are saying "if the digital root matches any of 0 or 1 or 3 or 4 or 6 or 7" in a more idiomatic way.
3. [`narrow`](https://docs.raku.org/routine/narrow) is a way to find the narrowest type a number fits into. `$N.sqrt` returns a [`Num`](https://docs.raku.org/type/Num) object, even if the value is an integer. This is the idiomatic way to check that the returned value is an integer.
  - I am glad I found this, because in the past I would have done something like `$N.sqrt.Int == $N.sqrt`, which requires me to duplicate computations.
4. [`hyper`](https://docs.raku.org/routine/hyper) allows us to perform some action (in this case `grep`) on a sequence _in parallel_ while still keeping the output in the original order of the sequence (see [`race`](https://docs.raku.org/routine/race) if order doesn't matter).
5. We are able to pass a function to `grep`. Since functions are first-class citizens in Raku, they come with their own [sigil](https://docs.raku.org/language/variables#index-entry-sigil_&), so we pass it in as `&function-name`. This is the equivalent of `.grep(-> $candidate { is-rare($candidate) })`, but easier to write.
  
## Task 2: Hash-counting String

You are given a positive integer `$N`.

Write a script to produce Hash-counting string of that length.

The definition of a hash-counting string is as follows:

- the string consists only of digits 0-9 and hashes, ‘#’
- there are no two consecutive hashes: ‘##’ does not appear in your string
- the last character is a hash
- the number immediately preceding each hash (if it exists) is the position of that hash in the string, with the position being counted up from 1

It can be shown that for every positive integer N there is exactly one such length-N string.

### Examples

```
(a) "#" is the counting string of length 1
(b) "2#" is the counting string of length 2
(c) "#3#" is the string of length 3
(d) "#3#5#7#10#" is the string of length 10
(e) "2#4#6#8#11#14#" is the string of length 14
```

### Solution

[GitHub Link](https://github.com/manwar/perlweeklychallenge-club/blob/master/challenge-102/aaronreidsmith/raku/ch-2.raku)

See below for explanation and any implementation-specific comments.

```
sub challenge(Int $N) returns Str {
    my @output;
    my $index = $N - 1;
    while $index >= 0 {
        @output[$index] = '#';
        my $position = $index + 1; # Position is 1-based while index is 0-based
        for $position.flip.comb.kv -> $offset, $digit {
            @output[$index - ($offset + 1)] = $digit;
        }
        $index -= ($position.chars + 1);
    }
    @output.join;
}

sub MAIN(Int $N) {
    say challenge($N);
}
```

This program runs as such:

```
$ raku ch-2.raku 14
2#4#6#8#11#14#
```

### Explanation

We are given two really concrete details about the sequence:

- the last character is a hash
- the number immediately preceding each hash (if it exists) is the position of that hash in the string, with the position being counted up from 1

Given that, we follow the following steps:

1. Define an array (`@output`) and start from the end (`$index = $N - 1`, since the array is 0-indexed).
2. While `$index` is greater-than-or-equal-to zero:
  - Set `@output[$index]` to `#`.
  - Find the 1-based index (`$position`) of that hash character (`$index + 1`).
  - Iterate **backwards** through the 1-based index and fill in the indices in front of the newly-placed `#` with the digits of `$position`.
  - Decrement `$index` by the amount of characters in `$position + 1` (the `1` is for the hash character).

#### Specific Comments

Nothing to add here; this one is pretty straight forward.

## Final Thoughts

It's pretty cool that Raku has `.sqrt` built right in, but I find it odd that it doesn't have some sort of `.is-whole` functionality (Python has `.is_integer()`, Scala has `.isWhole`). Maybe it does, and the documentation is just bad; it would not be the first time I have run into that! Honestly, if you read back through my blog, I think I have found 3 separate ways to check if a floating-point number (`Num`) is an integer (`Int`) in Raku. Oh well, I guess it is all part of the journey!