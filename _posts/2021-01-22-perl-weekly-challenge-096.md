---
title: "Perl Weekly Challenge 96"
categories:
  - Blog
tags:
  - Perl Weekly Challenge
  - Raku
---

I admittedly took a shortcut for part two this week, but it allowed me to introduce modules here (I don't _believe_ I have used them before in a blog), so I think it makes up for it. 🙂 

## Task 1: Reverse Words

You are given a string `$S`.

Write a script to reverse the order of words in the given string. The string may contain leading/trailing spaces. The string may have more than one space between words in the string. Print the result without leading/trailing spaces and there should be only one space between words.

### Example 1

```
Input: $S = "The Weekly Challenge"
Output: "Challenge Weekly The"
```

### Example 2

```
Input: $S = "    Perl and   Raku are  part of the same family  "
Output: "family same the of part are Raku and Perl"
```

### Solution

[GitHub Link](https://github.com/manwar/perlweeklychallenge-club/blob/master/challenge-096/aaronreidsmith/raku/ch-1.raku)

See below for explanation and any implementation-specific comments.

```
sub challenge(Str $S) returns Str {
    $S.trim.words.reverse.join(' ');
}

sub MAIN(Str $S) {
    say challenge($S);
}
```

This program runs as such:

```
$ raku ch-1.raku 'The Weekly Challenge'
Challenge Weekly The
```

### Explanation

Pretty easy one-liner here. Here is the logic:

1. Take the string and `trim` whitespace of the beginning and the end.
2. Split it into individual words using the handy `words` method (the equivalent of `split(/<space>+/)`).
3. Reverse the list generated from Step 2
4. Re-join the list into a space-separated string using `.join(' ')`.
  
## Task 2: Edit Distance

You are given two strings `$S1` and `$S2`.

Write a script to find out the minimum operations required to convert `$S1` into `$S2`. The operations can be "insert," "remove," or "replace" a character. Check out [Wikipedia page](https://en.wikipedia.org/wiki/Edit_distance) for more information.

### Example 1

```
Input: $S1 = "kitten"; $S2 = "sitting"
Output: 3

Explanation:
Operation 1: replace 'k' with 's'
Operation 2: replace 'e' with 'i'
Operation 3: insert 'g' at the end
```

### Example 2

```
Input: $S1 = "sunday"; $S2 = "monday"
Output: 2

Explanation:
Operation 1: replace 's' with 'm'
Operation 2: replace 'u' with 'o'
```

### Solution

[GitHub Link](https://github.com/manwar/perlweeklychallenge-club/blob/master/challenge-096/aaronreidsmith/raku/ch-2.raku)

See below for explanation and any implementation-specific comments.

```
use Text::Levenshtein; # imports `distance` # [1]

sub challenge(Str $S1, Str $S2) returns Int {
    distance($S1.lc, $S2.lc).head; # [2][3]
}

sub MAIN(Str $S1, Str $S2) {
    say challenge($S1, $S2);
}
```

This program runs as such:

```
$ raku ch-2.raku kitten sitting
3
```

### Explanation

This was definitely a cop-out. Edit distance is also known as [_Levenshtein Distance_](https://en.wikipedia.org/wiki/Levenshtein_distance); when an algorithm has someone's name attached to it, it is usually better to find an existing implementation. 😅 With that being said, if anyone _is_ interested in the Raku implementation of the algorithm, [here is the source code for `Text::Levenshtein`](https://github.com/thundergnat/Text-Levenshtein/blob/master/lib/Text/Levenshtein.pm6#L3-L28).

In case it is not obvious, we simply pass the input strings to `distance` and let it do the work.

#### Specific Comments

1. I encourage anyone reading this to read the [Raku documentation on modules](https://docs.raku.org/language/modules). Basically, `use` is one of several keywords to import modules, and is probably the most common you will see in the wild. You can import specific elements, if the author allows it, or you can write it as we did here and get the default imports.
2. `distance` will treat uppercase and lowercase letters differently, which I did not want, so we explicitly cast everything to lowercase (`.lc`) before passing them to `distance`.
3. `distance` will accept a variable number of arguments and compare the 2nd to Nth arguments to the first one, returning an array of Levenshtein distances. Since we only have two arguments, we need to extract the first (and only) distance in the array using `head`.

## Final Thoughts

In my day-to-day I always encourage folks to use modules where possible. In puzzles like these, I usually prefer to write my own implementation, even if it is less efficient. But it was a long week, so I took the lazy way out. 😉 See y'all next week!