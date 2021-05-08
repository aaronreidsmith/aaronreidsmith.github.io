---
title: "Perl Weekly Challenge 111"
categories:
  - Blog
tags:
  - Perl Weekly Challenge
  - Raku
---

I was apparently [the champion](https://perlweeklychallenge.org/blog/meet-the-champion-2021-04/) of the _Perl Weekly Challenge_ for last month, which is pretty cool! I encourage folks to go read my interview with Mohammad Anwar, who runs the _Perl Weekly Challenge_.

## Task 1: Search Matrix

You are given 5x5 matrix filled with integers such that each row is sorted from left to right, and the first integer of each row is greater than the last integer of the previous row.

Write a script to find a given integer in the matrix using an efficient search algorithm.

### Example

```
Matrix: [  1,  2,  3,  5,  7 ]
        [  9, 11, 15, 19, 20 ]
        [ 23, 24, 25, 29, 31 ]
        [ 32, 33, 39, 40, 42 ]
        [ 45, 47, 48, 49, 50 ]

Input: 35
Output: 0 since it is missing in the matrix

Input: 39
Output: 1 as it exists in the matrix
```

### Solution

[GitHub Link](https://github.com/manwar/perlweeklychallenge-club/blob/master/challenge-111/aaronreidsmith/raku/ch-1.raku)

See below for explanation and any implementation-specific comments.

```
sub challenge(@list-of-lists, Int $N) returns Int {
  my $output = 0;
  for (0..^@list-of-lists.end) Z (0^..@list-of-lists.end) -> ($i, $j) { # [1]
    if @list-of-lists[$i].head == $N || @list-of-lists[$j].head == $N { # [2]
      $output = 1;
      last;
    } elsif @list-of-lists[$i].head < $N < @list-of-lists[$j].head {
      $output = (any(@list-of-lists[$i][1..*]) ~~ $N).Int;              # [3]
      last;
    } elsif $j == @list-of-lists.end && $N > @list-of-lists[$j].head {  # [4]
      $output = (any(@list-of-lists[$j][1..*]) ~~ $N).Int;
      last;
    }
  }
  $output;
}

sub MAIN(Int $N) {
  my @list-of-lists = (   # [5]
    ( 1,  2,  3,  5,  7),
    ( 9, 11, 15, 19, 20),
    (23, 24, 25, 29, 31),
    (32, 33, 39, 40, 42),
    (45, 47, 48, 49, 50)
  );
  say challenge(@list-of-lists, $N);
}
```

This program runs as such:

```
$ raku ch-1.raku 35
0
```

### Explanation

I don't know if this is the most efficient method, but it is _an_ efficient method, which is what the question calls for. The naive solution would be something like this, which has a complexity of `O(n+k)` where `n` is the number of elements total (25) and `k` is the cost of flattening the structure (likely just 4 appends).

```
any(@list-of-lists.flat) ~~ $N
```

My approach, instead, looks at the first element of each sublist to determine if it should even bother looking in that sublist. If so, it will drop down and check items 2 through 5 of the sublist (I assume this happens in order using `any`). if not, it will skip the list entirely and jump to the next sublist.

I _think_ my approach has a complexity of `O(n+k)` where `n` is the number of sub-lists (5) and `k` is the number of elements in that list (minus the first one, so 4). So we will _at most_ do 9 checks and be able to determine if the item exists in a sublist. On average, we will have fewer checks than that.

#### Specific comments

1. This looks complex, but this is just making a list that looks like this `((0, 1), (1, 2), (2, 3), (3, 4))` so that we can look at two sublists at a time. The second sublist is necessary so we can check the top end of the range easily.
2. Check the head of the first list and head of the second sublist to see if we can skip searching a sublist.
3. If it is in the range of a sublist, we can drop into it and use `any`, which I am pretty sure just searches from left to right. At most this will search all 4 elements (we skip the `head` item), and will end early if it finds the element.
4. If this is the last iteration and we still haven't found `$N`, we need to drop into the last sublist, just for full coverage.
4. We could set this up to be dynamic and passed in at run time, but I figured it would be okay to hardcode for our purposes.
  
## Task 2: Ordered Letters

Given a word, you can sort its letters alphabetically (case-insensitive). For example, “beekeeper” becomes “beeeeekpr” and “dictionary” becomes “acdiinorty”.

Write a script to find the longest English words that don’t change when their letters are sorted.

### Solution

[GitHub Link](https://github.com/manwar/perlweeklychallenge-club/blob/master/challenge-111/aaronreidsmith/raku/ch-2.raku)

See below for explanation and any implementation-specific comments.

```
use LibCurl::HTTP :subs; # Imports jget

sub get-english-words {
  my %words = jget('https://raw.githubusercontent.com/dwyl/english-words/master/words_dictionary.json'); # [1]
  %words.keys;                                                                                           # [2]
}

sub challenge(Int $threshold) {
  my @words = get-english-words;
  my @matching-words = gather for @words.race -> $word {         # [3]
    my @chars = $word.comb;
    if @chars.elems >= $threshold && @chars.sort.join eq $word { # [4]
      take $word;
    }
  }
  @matching-words.sort;
}

multi sub MAIN(Int $threshold = 7) { # [5]
  for challenge($threshold) -> $word {
    say $word;
  }
}
```

This program runs as such:

```
$ raku ch-2.raku
adelops
aegilops
alloquy
beefily
begorry
belloot
billowy
deglory
egilops
```

### Explanation

So this question is pretty vague. The first problem we have is, how do we get a list of all English words? Rather than ship a text file around with my code, we can pull some at run time from an API. I couldn't find a decent free API, so I just found [this GitHub repo](https://github.com/dwyl/english-words) that has a JSON file full of words. Does it have all the words? I have no idea, but it will certainly work for our purposes.

Basically, once that is pulled down, we just split each word into characters, sort them, and compare them to the original word. However, we check against `$threshold` first, so we don't do the expensive computation on every word.

#### Specific Comments

1. Passing the `:sub` flag to `use LibCurl:HTTP` imports its individual subroutines, including `jget`. `jget` calls the URL and unpacks the returns JSON into a hash.
2. I don't know why the author of the above GitHub repo chose this format, but instead of using a JSON array, they used a format like this: `{"word": 1}`, so we only need the keys.
3. Since we need to process all of these words, and the order doesn't matter (since we will sort later), we can cast this list to a [`RaceSeq`](https://docs.raku.org/type/RaceSeq) that will process in parallel without definite order.
4. Check the threshold first, so we don't do the expensive computation if it is short. If it passes that check, sort the characters and compare to the original word. If it also passes that check, we can take this work and add it to our output.
5. The question asks us to find the longest English **words** (plural). The single longest word is 8 characters (`aegilops`, which is a [genus of plant](https://en.wikipedia.org/wiki/Aegilops)), so I bumped the threshold down to 7 to give the longest English **words**.

## Final Thoughts

I have never gotten to do web requests in Raku, so it was fun learning about different packages for that. There is even the [`Cro`](https://cro.services/) project for setting up APIs; maybe I will get a chance to use that in the future. See y'all next week!
