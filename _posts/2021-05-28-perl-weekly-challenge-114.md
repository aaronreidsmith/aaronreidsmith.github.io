---
title: "Perl Weekly Challenge 114"
categories:
  - Blog
tags:
  - Perl Weekly Challenge
  - Raku
---

Both of this week's solutions look remarkably similar, because we were able to utilize the `first` subroutine for each one!

## Task 1: Next Palindrome Number

You are given a positive integer `$N`.

Write a script to find out the next Palindrome Number higher than the given integer `$N`.

### Example

```
Input: $N = 1234
Output: 1331

Input: $N = 999
Output: 1001
```

### Solution

[GitHub Link](https://github.com/manwar/perlweeklychallenge-club/blob/master/challenge-114/aaronreidsmith/raku/ch-1.raku)

See below for explanation and any implementation-specific comments.

```
sub challenge(Int $N) returns Int {
  ($N^..Inf).first(-> $num { $num == $num.flip }, :v); # [1][2][3]
}

sub MAIN(Int $N) {
  say challenge($N);
}
```

This program runs as such:

```
$ raku ch-1.raku 1234
1331
```

### Explanation

This is fairly straightforward; we create an infinite range from `$N` to infinity. This range will be lazily evaluated, so we don't have to worry about memory. Then we find the first instance where `$num` is equal to `$num.flip`. That's it!

#### Specific comments

1. Ranges are lazily evaluated, so it is safe to have these seemingly infinite range constructors.
2. `$num.flip` _technically_ returns a string, but `==` will coerce it to an integer (since `eq` should be used for string equality). This is convenient, but also kind of scary that conversions are happening without us knowing.
3. `first` returns both the index and value of that index by default. Since we only want the value, we pass in the `:v` flag to specify that.
  
## Task 2: Higher Integer Set Bits

You are given a positive integer `$N`.

Write a script to find the next higher integer having the same number of 1 bits in binary representation as `$N`.

### Example

```
Input: $N = 3
Output: 5

Binary representation of $N is 011. There are two 1 bits. So the next higher integer is 5 having the same the number of 1 bits i.e. 101.

Input: $N = 12
Output: 17

Binary representation of $N is 1100. There are two 1 bits. So the next higher integer is 17 having the same number of 1 bits i.e. 10001.
```

### Solution

[GitHub Link](https://github.com/manwar/perlweeklychallenge-club/blob/master/challenge-114/aaronreidsmith/raku/ch-2.raku)

See below for explanation and any implementation-specific comments.

```
sub bits(Int $base-ten) returns Int {
  $base-ten.base(2).comb.grep(* eq '1').elems; # [1][2][3][4]
}

sub challenge(Int $N where $N > 0) returns Int {
  my $bits = bits($N);
  ($N^..Inf).first(-> $num { bits($num) == $bits }, :v);
}

sub MAIN(Int $N) {
  say challenge($N);
}
```

This program runs as such:

```
$ raku ch-2.raku 12
17
```

### Explanation

The meat of this lies in the `bits` function. It finds the number of `1` bits for a given integer. Given that, we again construct a range from `$N` to infinity and find the first number that has the same number of bits as `$N`.

#### Specific Comments

1. [`base`](https://docs.raku.org/routine/base) is a cool function to convert a number to any other base. So `9.base(3) eq '100'` and `255.base(16) eq 'FF'`. We use it to convert base 10 to base 2.
2. Once we have it in base 2, we need to convert it to a list of digits, so we use `comb`.
3. Once it has been converted to a list of digits, we filter (`grep`) for digits that equal `1`. Since `base` converted to a string, we use string equality (`eq`).
4. Finally, we just count the elements that equal `1` using `elems`.

## Final Thoughts

Lazy evaluation is one of the pillars of functional programming, so it is cool to see it exist in Raku. Always happy when I can break these down into a line or two!
