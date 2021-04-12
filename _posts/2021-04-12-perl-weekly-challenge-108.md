---
title: "Perl Weekly Challenge 108"
categories:
  - Blog
tags:
  - Perl Weekly Challenge
  - Raku
---

Task 1 this week is kind of a joke, but task 2 was interesting!

## Task 1: Locate Memory

Write a script to declare a variable or constant and print its location in the memory.

### Solution

[GitHub Link](https://github.com/manwar/perlweeklychallenge-club/blob/master/challenge-108/aaronreidsmith/raku/ch-1.raku)

See below for explanation and any implementation-specific comments.

```
sub challenge(Any $variable) returns Int {
    $variable.WHERE;
}

sub MAIN {
    my $variable = rand;      # [1][2]
    say challenge($variable);
}
```

This program runs as such:

```
$ raku ch-1.raku
140444494947864
```

### Explanation

Raku has the [`WHERE`](https://docs.raku.org/routine/WHERE) method built into it that "Returns an `Int` representing the memory address of the object," we simply need to utilize that.

#### Specific comments

1. `rand` is a built-in subroutine that returns a random integer.
2.  Following the Scala style, I would normally use parentheses for subroutines that are not "pure" and write this as `rand()`, but Raku complains with the following error: `Unsupported use of rand().  In Raku please use: rand.`
  
## Task 2: Bell Numbers

Write a script to display top 10 Bell Numbers. Please refer to the [Wikipedia page](https://en.wikipedia.org/wiki/Bell_number) for more information.

### Example

- B<sub>0</sub>: 1, as you can only have one partition of zero element set.
- B<sub>1</sub>: 1, as you can only have one partition of one element set `{a}`.
- B<sub>2</sub>: 2

  ```
  {a}{b}
  {a,b}
  ```
  
- B<sub>3</sub>: 5

  ```
  {a}{b}{c}
  {a,b}{c}
  {a}{b,c}
  {a,c}{b}
  {a,b,c}
  ```
  
- B<sub>4</sub>: 15

  ```
  {a}{b}{c}{d}
  {a,b,c,d}
  {a,b}{c,d}
  {a,c}{b,d}
  {a,d}{b,c}
  {a,b}{c}{d}
  {a,c}{b}{d}
  {a,d}{b}{c}
  {b,c}{a}{d}
  {b,d}{a}{c}
  {c,d}{a}{b}
  {a}{b,c,d}
  {b}{a,c,d}
  {c}{a,b,d}
  {d}{a,b,c}
  ```

### Solution

[GitHub Link](https://github.com/manwar/perlweeklychallenge-club/blob/master/challenge-108/aaronreidsmith/raku/ch-2.raku)

See below for explanation and any implementation-specific comments.

```
use experimental :cached;

sub challenge(Int $n where $n >= 0) is cached returns Int {            # [1]
    given $n {
        when 0|1 { 1 }
        default {
            my $n-minus-one = $n - 1;
            gather for (0..$n-minus-one) -> $k {                       # [2]
                take (^$n-minus-one).combinations($k) * challenge($k); # [2]
            }.sum
        }
    }
}

sub MAIN(Int $n = 10) {
    say (^$n).map(&challenge);
}
```

This program runs as such:

```
$ raku ch-2.raku
(1 1 2 5 15 52 203 877 4140 21147)
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

**Note:** The question asks for the "top 10 Bell Numbers." Since this is an ever-increasing sequence, there is no "top," so I interpreted that to mean _first_ 10 Bell numbers.

At first glance, this code has nothing to do with the input sequences, but digging into the above-linked Wikipedia entry, we find this equation:

$ B\_{n+1} = \sum\_{k=0}^{n}{n \choose k}B\_{k} $

This tells us that each Bell number is built upon by the previous Bell numbers. And we know the first two Bell numbers, so we can follow this.

Let's re-write this to calculate $ B\_{2} $ and see how it works; remember, since we are calculating for $ B\_{n+1} $, we use $ n = 1 $.

$ B\_{2} = \sum\_{k=0}^{1}{1 \choose k}B\_{k} $

Which can be expanded as:

$ B\_{2} = {1 \choose 0}B\_{0} + {1 \choose 1}B\_{1} $

Which can be reduced to:

$ B\_{2} = (1)(1) + (1)(1) = 2 $

So $ B\_{2} = 2 $ and we can use that to calculate $ B\_{3} $ and so on.

Now that we have the algorithm figured out, and decided we are going to apply it to the _first_ 10 terms, it's a simple matter to `map` the function over the sequence from 0 (inclusive) to 10 (exclusive).


#### Specific Comments

1. Since this is a recursive function, once we calculate $ B\_{2} $ we will use it in $ B\_{3} $, $ B\_{4} $ and so on. No use re-calculating it every time, so we memoize this function using the `is cached` trait.
2. gather/take is a construct to build up a sequence using a `Supply` (in this case, the `for` loop). 

## Final Thoughts

I love me some pattern matching and recursion, coming from a Scala day job, so it is fun to use those constructs in other languages, especially Raku. 🙂
