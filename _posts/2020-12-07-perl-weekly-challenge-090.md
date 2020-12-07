---
title: "Perl Weekly Challenge 90"
categories:
  - Blog
tags:
  - Perl Weekly Challenge
  - Raku
---

Today was a busy day with both [Advent of Code](https://aaronreidsmith.github.io/blog/advent-of-code-day-07/) and the Perl Weekly Challenge. Luckily, the PWC was short and sweet this week, and a nice breather after the Advent of Code.

## Task 1: DNA Sequence

You are given DNA sequence, GTAAACCCCTTTTCATTTAGACAGATCGACTCCTTATCCATTCTCAGAGATGTGTTGCTGGTCGCCG.

Write a script to print nucleotide count in the given DNA sequence. Also print the complementary sequence where Thymine (T) on one strand is always facing an adenine (A) and vice versa; guanine (G) is always facing a cytosine (C) and vice versa.

### Solution

[GitHub Link](https://github.com/manwar/perlweeklychallenge-club/blob/master/challenge-090/aaronreidsmith/raku/ch-1.raku)

See below for explanation and any implementation-specific comments.

```
subset ValidDna of Str where { $_ ~~ /^^[A|T|G|C]+$$/ }

sub MAIN($dna where $dna ~~ ValidDna, Bool :rc(:$reverse-complement) = False) { # [1]
    say "Input stats:\n{$dna.comb.Bag.Hash}\n";                                 # [2]

    say "Complement:";
    my $translated = $dna.trans('ATGC' => 'TACG');                              # [3]
    if $reverse-complement {
        say "5'-{$translated.flip}-3'";
    } else {
        say "3'-$translated-5'"
    }
}
```

This program runs as such:

```
$ raku ch-1.raku GTAAACCCCTTTTCATTTAGACAGATCGACTCCTTATCCATTCTCAGAGATGTGTTGCTGGTCGCCG
Input stats:
A	14
C	18
G	13
T	22

Complement:
3'-CATTTGGGGAAAAGTAAATCTGTCTAGCTGAGGAATAGGTAAGAGTCTCTACACAACGACCAGCGGC-5'

$ raku ch-1.raku --reverse-complement GTAAACCCCTTTTCATTTAGACAGATCGACTCCTTATCCATTCTCAGAGATGTGTTGCTGGTCGCCG
Input stats:
A	14
C	18
G	13
T	22

Complement:
5'-CGGCGACCAGCAACACATCTCTGAGAATGGATAAGGAGTCGATCTGTCTAAATGAAAAGGGGTTTAC-3'
```

### Explanation

Coming from a Biochemistry background, this one is rather simple. However, the question does not take into consideration that DNA has a [direction](https://en.wikipedia.org/wiki/Directionality_(molecular_biology)). Generally, if you are handed a string like this, you expect it to be read from 5' to 3' (5 prime to 3 prime). Because of the directionality, the opposite strand would be 3' to 5'.

So generally, when a question asks for the complementary strand, they want the _reverse_ complement, so it is shown 5' to 3'. This question did not specify, so I wrote an answer that handles both.

#### Specific comments

1. This syntax allows us to give aliases to our command line arguments. In this case, we accept either `--rc` or `--reverse-complement` and store it in a variable called `$reverse-complement`.
2. A [`Bag`](https://docs.raku.org/type/Bag) is a weighted collection. When passed the `List` produced by `.comb`, it generates a bag with the weight of each letter. We only convert it to a `Hash` for pretty printing.
3. Raku's `trans` method is a single-pass method, meaning you won't translate `A` to `T` and then accidentally translate it back to `A` with a second pass.

  
## Task 2: Ethiopian Multiplication

You are given two positive numbers `$A` and `$B`.

Write a script to demonstrate [Ethiopian Multiplication](https://threesixty360.wordpress.com/2009/06/09/ethiopian-multiplication/) using the given numbers.

### Solution

[GitHub Link](https://github.com/manwar/perlweeklychallenge-club/blob/master/challenge-090/aaronreidsmith/raku/ch-2.raku)

See below for explanation and any implementation-specific comments.

```
subset PositiveInt of Int where { $_ ~~ Int && $_ > 0 }

sub generate-pairs($a, $b) {
    sprintf("%02d, %02d", $a, $b).put;
    if $a == 1 {
        (($a, $b),);
    } else {
        (($a, $b), |generate-pairs($a div 2, $b * 2));
    }
}

sub MAIN(PositiveInt $A, PositiveInt $B) {
    say "Input: A: $A, B: $B";
    say "Divide A by 2 (ignoring remainders) until it is 1. Multiply B by 2 as we go:";
    my @pairs = generate-pairs($A, $B);
    say "Then, wherever A is odd, we add the Bs together:";
    my @odd-bs = @pairs.grep(-> @pair { !(@pair[0] %% 2) }).map(-> @pair { @pair[1] });
    say "{@odd-bs.join(' + ')} = {@odd-bs.sum}";
}
```

This program runs as such:

```
$ raku ch-2.raku 14 12
Input: A=14, B=12
Divide A by 2 (ignoring remainders) until it is 1. Multiply B by 2 as we go:
14, 12
07, 24
03, 48
01, 96
Then, wherever A is odd, we add the Bs together:
24 + 48 + 96 = 168
```

### Explanation

This is a very straightforward solution; most of the mess in the code is from the messages printed out. Basically, we generate our pairs (and print them) using recursion, then filter them down to where `$A` is odd, and add up the `$B`s.

## Final Thoughts

This week was super easy, so not much to add! Jump over to my blog on [day 7 of the Advent of Code](https://aaronreidsmith.github.io/blog/advent-of-code-day-07/) for something more challenging.