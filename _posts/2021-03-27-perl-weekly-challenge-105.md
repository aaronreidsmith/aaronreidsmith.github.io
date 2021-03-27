---
title: "Perl Weekly Challenge 105"
categories:
  - Blog
tags:
  - Perl Weekly Challenge
  - Raku
---

This week's challenges are short and sweet, but still give us the opportunity to explore some interesting Raku-isms!

## Task 1: Nth root

You are given positive numbers `$N` and `$k`.

Write a script to find out the `$N`th root of `$k`. For more information, please take a look at the [wiki page](https://en.wikipedia.org/wiki/Nth_root#Computing_principal_roots).

### Examples

```
Input: $N = 5, $k = 248832
Output: 12

Input: $N = 5, $k = 34
Output: 2.02
```

### Solution

[GitHub Link](https://github.com/manwar/perlweeklychallenge-club/blob/master/challenge-105/aaronreidsmith/raku/ch-1.raku)

See below for explanation and any implementation-specific comments.

```
sub challenge(Numeric $N, Numeric $k) returns Str { # [1]
    my $root = $k ** (1 / $N);
    $root.round(.01).Str;                           # [2]
}

sub MAIN(Num $N, Num $k) {
    say challenge($N, $k);
}
```

This program runs as such:

```
$ raku ch-1.raku 5 248832
12
```

### Explanation

<!-- Allow inlining of math functionality -->
<script type="text/x-mathjax-config">
  MathJax.Hub.Config({
    tex2jax: {
      inlineMath: [ ['$','$'], ["\\(","\\)"] ],
      processEscapes: true
    }
  });
</script>

<!-- Import math functionality -->
<script type="text/javascript" async
  src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-MML-AM_CHTML">
</script>


This solution relies on the fact that $ \sqrt[N]{k} $ can be rewritten as $ k^{1/N} $ (which is `$k ** (1 / $N)` in Raku). So we simply have to do that and round to the appropriate amount of decimal places (the example shows 2 or less, so that is what we do as well).

#### Specific comments

1. The examples just show integers, but this function should theoretically be able to take any numeric value, so we use [`Numeric`](https://docs.raku.org/type/Numeric) for both of our input types.
2. Raku's [round](https://docs.raku.org/routine/round) function is interesting in that you don't specify the number of decimals, you specify some arbitrary scale, and it will round to the _closest multiple of that scale_. So `1` would round to an integer and `.01` would round to two decimals. Additionally, it will drop trailing zeros (and even the decimal if the rounded number only has zeros as decimals).
  
## Task 2: The Name Game

You are given a `$name`.

Write a script to display the lyrics to the Shirley Ellis song The Name Game. Please checkout the wiki page for more information.

```
Input: $name = "Katie"
Output:

    Katie, Katie, bo-batie,
    Bonana-fanna fo-fatie
    Fee fi mo-matie
    Katie!
```

### Solution

[GitHub Link](https://github.com/manwar/perlweeklychallenge-club/blob/master/challenge-105/aaronreidsmith/raku/ch-2.raku)

See below for explanation and any implementation-specific comments.

```
sub challenge(Str $name) returns Str {
    my $X = $name.wordcase;                                             # [1]
    my $Y = $X ~~ /^[A|E|I|O|U|Y]<-[aeiouy]>/ ?? $X.lc !! $X.substr(1); # [2]

    qq:to/END/;                                                         # [3]
    $X, $X, bo-{$X.starts-with('B') ?? '' !! 'b'}$Y                     # [4]
    Bonana-fanna fo-{$X.starts-with('F') ?? '' !! 'f'}$Y
    Fee fi mo-{$X.starts-with('M') ?? '' !! 'm'}$Y
    $X!
    END
}

sub MAIN(Str $name) {
    say challenge($name);
}
```

This program runs as such:

```
$ raku ch-2.raku Aaron
Aaron, Aaron, bo-baron
Bonana-fanna fo-faron
Fee fi mo-maron
Aaron!
```

### Explanation

According to the wikipedia page, the structure can be broken down like this:

```
(X), (X), bo-b(Y)
Bonana-fanna fo-f(Y)
Fee fi mo-m(Y)
(X)!
```

The only caveat it adds is:

```
If the name starts with a b, f, or m, that sound simply is not repeated. For example: Billy becomes "Billy Billy bo-illy"; Fred becomes "bonana fanna fo-red"; Marsha becomes "fee fi mo-arsha"
```

I actually don't think this caveat is enough. For example, my son's name is Everett, and if we just cut off the first letter of his name as the wiki suggests, we would get things like `bverett` or `fverett`. So, I added an additional stipulation: any name that starts with a vowel followed by a consonant should keep the _entirety_ of the name as `Y`, otherwise it is just `X` minus the first letter.

Once we have found `X` and `Y`, we just slot them into the song. Easy peasy!

#### Specific Comments

1. [`wordcase`](https://docs.raku.org/routine/wordcase) makes the first letter uppercase, and the rest lowercase.
2. This checks to see if the first letter is a vowel (including `Y`) directly followed a consonant. If that is the case, keep the entirety of `$X` and just convert it to lowercase to make sense in the song. Otherwise, take the [substring](https://docs.raku.org/routine/substr) of `$X` from index 1 to the end.
3. [`qq`](https://docs.raku.org/language/quoting#Heredocs:_:to) is an easy way to make multi-line strings that include interpolation. In this case, we say "the rest of this up until `END` is a literal string." Additionally, since all lines are indented to the same depth, it strips of leading indentation.
4. Since this whole construct is interpolated, we are able to embed the special cases for `B`, `F`, and `M` directly into the output string.

## Final Thoughts

Like I said, short and sweet! See y'all next week!
