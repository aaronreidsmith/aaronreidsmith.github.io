---
title: "Perl Weekly Challenge 97"
categories:
  - Blog
tags:
  - Perl Weekly Challenge
  - Raku
---

My solution to challenge two builds on last week's challenge two, so I encourage you to go read [last week's post](https://aaronreidsmith.github.io/blog/perl-weekly-challenge-096/) if you haven't already!

## Task 1: Caesar Cipher


You are given string `$S` containing alphabets `A..Z` only and a number `$N`.

Write a script to encrypt the given string `$S` using a [Caesar Cipher](https://en.wikipedia.org/wiki/Caesar_cipher) with left shift of size `$N`.

### Example

```
Input: $S = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG", $N = 3
Output: "QEB NRFZH YOLTK CLU GRJMP LSBO QEB IXWV ALD"

Plain:  ABCDEFGHIJKLMNOPQRSTUVWXYZ
Cipher: XYZABCDEFGHIJKLMNOPQRSTUVW

Plaintext:  THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG
Ciphertext: QEB NRFZH YOLTK CLU GRJMP LSBO QEB IXWV ALD
```

### Solution

[GitHub Link](https://github.com/manwar/perlweeklychallenge-club/blob/master/challenge-097/aaronreidsmith/raku/ch-1.raku)

See below for explanation and any implementation-specific comments.

```
constant @alphabet = ('A'..'Z').List; # [1]

sub challenge(
    Str $S where $S ~~ /^[<alpha>|<space>]+$/, # [2]
    Int $N where $N >= 0
) {
    $S.uc.trans(@alphabet => @alphabet.rotate(-$N)); # [3][4]
}

sub MAIN(Str $S, Int $N) {
    say challenge($S, $N);
}
```

This program runs as such:

```
$ raku ch-1.raku 'THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG' 3
QEB NRFZH YOLTK CLU GRJMP LSBO QEB IXWV ALD
```

### Explanation

We use some cool built-in functionality to make this so simple. Here is the logic:

1. Make sure the string is uppercase (`.uc`). They say we will always get uppercase, but might as well validate.
2. For each letter in the string, translate it to a different version of the alphabet that is rotated by `$N` spaces.

That's it!

#### Specific comments

1. Since the alphabet is always going to be constant we can instantiate it at the top level as a [`constant`](https://docs.raku.org/language/terms#Constants). Constants are evaluated at compile time, so this speeds up the program (even if just marginally).
2. You have likely seen me use this syntax before; these are called anonymous type constraints, and allow us to be a little more specific than just `Str` or `Int`. In this case, we want a string that only contains letters and spaces, and an int that is greater than or equal to zero.
3. [`trans`](https://docs.raku.org/routine/trans) is a cool subroutine; it takes two lists (or strings) defining replacements to be made in the supplied string. Given the example above, it is the equivalent of something like `$S.subst('a', 'x').subst('b', 'y')...`. The left argument, in our case, will always be the alphabet, and the right argument is the alphabet rotated by `$N` spaces.
4. [`rotate`](https://docs.raku.org/routine/rotate) takes a list and rotates it to the left. Since we need our letters shifted to the right, we use a negative number (`-$N`).
  
## Task 2: Binary Substrings

You are given a binary string `$B` and an integer `$S`.

Write a script to split the binary string `$B` of size `$S` and then find the minimum number of flips required to make it all the same.

### Example 1

```
Input: $B = “101100101”, $S = 3
Output: 1

Binary Substrings:
  "101": 0 flip
  "100": 1 flip to make it "101"
  "101": 0 flip
```

### Example 2

```
Input $B = “10110111”, $S = 4
Output: 2

Binary Substrings:
  "1011": 0 flip
  "0111": 2 flips to make it "1011"
```

### Solution

[GitHub Link](https://github.com/manwar/perlweeklychallenge-club/blob/master/challenge-097/aaronreidsmith/raku/ch-2.raku)

See below for explanation and any implementation-specific comments.

```
use Text::Levenshtein; # imports `distance`

sub challenge(
    Str $B where $B ~~ /^[0|1]+$/,
    Int $S where $S > 0
) {
    my @segments = $B.comb.rotor($S, :partial).map(-> @chars { # [1]
        my $segment = @chars.join;
        $segment ~ '0' x ($S - $segment.chars) # [2][3]
    });
    distance(|@segments).sum; # [4]
}

multi sub MAIN(Str $B, Int $S) {
    say challenge($B, $S);
}
```

This program runs as such:

```
$ raku ch-2.raku 101100101 3
1
```

### Explanation

The number of flips seems oddly similar to the edit distance from last week, no? I was able to reuse `Text::Levenshtein.distance` from last week to find the "edit distance" between binary strings! We do a little work to split the string into `$S` pieces (padding with zeros, if necessary), then leave all the heaving lifting to `distance`.

#### Specific Comments

1. [`rotor`](https://docs.raku.org/routine/rotor) splits a list into pieces based on the argument (`$S` in this case). We pass it the `:partial` flag so that it keeps any pieces that are less than `$S` in size (rather than throwing them away).
2. [`~`](https://docs.raku.org/routine/~) is Raku's string concatenation subroutine.
3. [`x`](https://docs.raku.org/routine/x) is Raku's string repetition operator. I couldn't an `rpad` method in Raku, so this is my workaround.
4. `distance` does not take a single list of arguments, it takes a variable amount of top-level arguments. To achieve that behavior, we use a [slip (`|`)](https://docs.raku.org/routine/%7C) to unpack the list we built.
 
## Final Thoughts

As I was writing this blog I realized it may have been better for me to left pad the binary strings in challenge two; `1001 != 100100` but `1001 == 001001`. Oh well, the question doesn't talk about the "partial" case anyway!