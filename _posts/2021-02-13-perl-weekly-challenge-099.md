---
title: "Perl Weekly Challenge 99"
categories:
  - Blog
tags:
  - Perl Weekly Challenge
  - Raku
---

This week's theme is [_regex_](https://en.wikipedia.org/wiki/Regular_expression), which is something the Perl family of languages has always been known for.

## Task 1: Pattern Match

You are given a string `$S` and a pattern `$P`.

Write a script to check if the given pattern matches the entire string. Print `1` if so, otherwise `0`.

The patterns can also have the following characters:

`?` - Match any single character.  
`*` - Match any sequence of characters.

### Example 1
```
Input: $S = "abcde" $P = "a*e"
Output: 1
```

### Example 2

```
Input: $S = "abcde" $P = "a*d"
Output: 0
```

### Example 3

```
Input: $S = "abcde" $P = "?b*d"
Output: 0
```

### Example 4

```
Input: $S = "abcde" $P = "a*c?e"
Output: 1
```

### Solution

[GitHub Link](https://github.com/manwar/perlweeklychallenge-club/blob/master/challenge-099/aaronreidsmith/raku/ch-1.raku)

See below for explanation and any implementation-specific comments.

```
sub challenge(Str $S, Str $P) returns Int {
    my $regex = '^' ~ $P.trans(['*', '?'] => ['.*', '.']) ~ '$'; # [1][2][3]
    ($S ~~ /<$regex>/).Bool.Int;                                 # [4][5]
}

sub MAIN(Str $S, Str $P) {
    say challenge($S, $P);
}
```

This program runs as such:

```
$ raku ch-1.raku abcde a*e
1
```

### Explanation

This one is pretty simple -- we essentially just translate our pattern characters to their regex counterparts (see table below), then check if it matches `$S`. If so, we return `1`, otherwise `0`.

|Pattern Character|Regex Counterpart|Meaning|
|---|---|---|
|`?`|`.`|Any single character|
|`*`|`.*`|Any single character _zero or more times_ (the `*` means "zero or more" in regex)|

#### Specific comments

1. The question says the pattern has to match the entire string, so we add `^` (which means "start of string") and `$` (which means "end of string") to the pattern.
2. The [`trans`](https://docs.raku.org/routine/trans) method can take either two strings or two lists. If we provide two strings, they must be of the same length. Since one of our characters maps to _two_ regex characters (`*` -> `.*`), we have to use the list style.
3. `~` is the Raku [concatenate operator](https://docs.raku.org/routine/~) so that we create just one string.
4. To reference a regex stored in a variable, we have to use the [bracket notation](https://docs.raku.org/language/regexes#Regex_interpolation).
5. The [smart match operator](https://docs.raku.org/routine/~~) (`~~`) returns a [`Match`](https://docs.raku.org/type/Match) object, which we cast to a boolean (to see _if_ it matched) and then an integer (a boolean will cast to `0` if false, and `1` if true).
  
## Task 2: Unique Subsequence

You are given two strings `$S` and `$T`.

Write a script to find out count of different unique subsequences matching `$T` without changing the position of characters.

### Example 1

```
Input: $S = "littleit', $T = 'lit'
Output: 5

    1: [lit] tleit
    2: [li] t [t] leit
    3: [li] ttlei [t]
    4: litt [l] e [it]
    5: [l] ittle [it]
```

### Example 2

```
Input: $S = "london', $T = 'lon'
Output: 3

    1: [lon] don
    2: [lo] ndo [n]
    3: [l] ond [on]
```

### Solution

[GitHub Link](https://github.com/manwar/perlweeklychallenge-club/blob/master/challenge-099/aaronreidsmith/raku/ch-2.raku)

See below for explanation and any implementation-specific comments.

```
sub challenge(Str $S, Str $T) returns Int {
    my $regex = $T.comb.join('.*');     # [1]
    ($S ~~ m:exhaustive/<$regex>/).Int; # [2][3]
}

sub MAIN(Str $S, Str $T) {
    say challenge($S, $T);
}
```

This program runs as such:

```
$ raku ch-2.raku littleit lit
5
```

### Explanation

We basically take our `$T` and convert it to a regex that looks like this: `l.*i.*t`. Which, as we know from Task 1, means that we want to match the word `lit` with _zero or more characters_ between each letter. We then do an exhaustive match against `$S` and count the number of matches.

#### Specific Comments

1. `comb` converts the string to a list of characters (i.e. `'foo'` -> `['f', 'o', 'o']`), which we then join together with our `.*` regex.
2. We supply the [`exhaustive` adverb](https://docs.raku.org/language/regexes#Adverbs) (we have to say this is a `match` adverb with `m`, or else it would think it is a _regex_ adverb), which tells the regex to keep going after the first match and find an exhaustive list of matches.
3. Calling `.Int` on a match object directly will return the number of matches it found.
 
## Final Thoughts

Perl has always been the king of regex, which is why it got (and continues to stay) so popular. Raku continues that legacy and made these problems relatively simple.