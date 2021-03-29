---
title: "Perl Weekly Challenge 106"
categories:
  - Blog
tags:
  - Perl Weekly Challenge
  - Raku
---

Task 2 _seems_ like it would be difficult, but once again, Raku has built-in mechanisms to help us out!

## Task 1: Maximum Gap

You are given an array of integers `@N`.

Write a script to display the maximum difference between two successive elements once the array is sorted.

If the array contains only 1 element then display 0.

### Examples

```
Input: @N = (2, 9, 3, 5)
Output: 4

Input: @N = (1, 3, 8, 2, 0)
Output: 5

Input: @N = (5)
Output: 0
```

### Solution

[GitHub Link](https://github.com/manwar/perlweeklychallenge-club/blob/master/challenge-106/aaronreidsmith/raku/ch-1.raku)

See below for explanation and any implementation-specific comments.

```
sub challenge(@N where all(@N) ~~ Int) returns Int {   # [1]
    if @N.elems == 1 {
        0;
    } else {
        my @sorted = @N.sort;
        my @zipped = @sorted[0..*-1] Z @sorted[1..*];  # [2]
        @zipped.map(-> ($a, $b) { abs($b - $a) }).max; # [3]
    }
}

sub MAIN(*@N where all(@N) ~~ Int) {
    say challenge(@N);
}
```

This program runs as such:

```
$ raku ch-1.raku 2 9 3 5
4
```

### Explanation

This one is probably easier to walk through with an example. If `@N` only has one element, we just return `0`, so we won't discuss that path.

1. We get this input: `@N = (2, 9, 3, 5)`.
2. We sort it so we have `@sorted = (2, 3, 5, 9)`.
3. We generate two lists: One of everything but the last element (`@sorted[0..*-1] = (2, 3, 5)`) and one of everything but the first element (`@sorted[1..*] = (3, 5, 9)`). Then we zip them together so we have `@zipped = ((2, 3), (3, 5), (5, 9))`.
4. For each pair, we find the difference between the numbers, so we end up with this: `(1, 2, 4)`.
5. Finally, we call `.max` and return the maximum difference, which is `4` in this case.

#### Specific comments

1. Raku has so many different sequence types (`Positional`, `Array`, `List`, `Seq`, etc.) that I have not figured out a good way to parameterize positional inputs. This is the best I can come up with, but for long sequences, it is incredibly slow.
2. The "whatever star" is signaling the last index of the list, in this case. So we are simply generating a list containing everything but the last item zipped with a list containing everything but the last item (see above for example).
3. In theory, we could have negative numbers in our input, so it is necessary to have the call to `abs`.
  
## Task 2: Decimal String

You are given a numerator and denominator i.e. `$N` and `$D`.

Write a script to convert the fraction into decimal string. If the fractional part is recurring then put it in parentheses.

```
Input: $N = 1, $D = 3
Output: "0.(3)"

Input: $N = 1, $D = 2
Output: "0.5"

Input: $N = 5, $D = 66
Output: "0.0(75)"
```

### Solution

[GitHub Link](https://github.com/manwar/perlweeklychallenge-club/blob/master/challenge-106/aaronreidsmith/raku/ch-2.raku)

See below for explanation and any implementation-specific comments.

```
sub challenge(Numeric $N, Numeric $D) returns Str {                  # [1]
    my ($base, $repeating) = ($N / $D).base-repeating;               # [2]
    $repeating = $repeating eq '' ?? $repeating !! "\($repeating\)"; # [3]
    $base ~ $repeating;                                              # [4]
}

sub MAIN(Numeric $N, Numeric $D) {
    say challenge($N, $D);
}
```

This program runs as such:

```
$ raku ch-2.raku 1 7
0.(142857)
```

### Explanation

This looks suspiciously small for what seems like a complex problem. All the logic happens in `base-repeating` (which I will detail below). All we have to do is supply the `$N` and `D`, and the rest of the code is just for formatting!

#### Specific Comments

1. In theory someone could pass in arbitrary decimal numbers, so we accept `Numeric` instead of just `Int`.
2. [`base-repeating`](https://docs.raku.org/routine/base-repeating) operates on a [`Rational`](https://docs.raku.org/type/Rational), which is Raku's way of saying fraction. It splits the fraction into pieces -- the base and the repeating portion. For something like `5 / 2`, it would return `('2.5', '')`. For something like `1 / 3`, we would get `'0.', '3')`. Once we have that, we just have to format like the question asks.
3. If the repeated section is empty, we want to just leave it alone. Otherwise, we want to wrap it in parentheses as the challenge states.
4. We could also have written `"$base$repeating"` to concatenate the pieces, but that is harder to read, so I used the string concatenation operator (`~`).

## Final Thoughts

I don't know whether or not to consider it cheating when Raku has all the cool built-ins. I guess we're just using the tools we are provided, but it feels too easy. 😅
