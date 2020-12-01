---
title: "Advent of Code: Day 1"
last_modified_at: 2020-12-01T08:40:30-05:00
categories:
  - Blog
tags:
  - Advent of Code
  - Raku
---

Turns out I started blogging just in time for the [Advent of Code](https://adventofcode.com/), an annual series of daily challenges that run from December 1st to December 25th.

These problems remind me a lot of [Project Euler](https://projecteuler.net/), because they are not concerned with the readbility or speed of your code, just the output. That means that any goals one wishes to accomplish should be set personally (there _is_ technically a leaderboard, but I find you have to be online very late at night to catch the posts and it is not worth the stress during the holiday season).

My goal, as you may have guessed from my previous posts, is to complete these challenges in _at least_ Raku and to do so utilizing a functional programming paradigm. Let's dive into day 1 and see if I can do it!

## The Problem

I am not going to copy and paste the explanation of the problem here like I do for the Perl Weekly Challenge, because it is _so_ long and I want to encourage users to go attempt the challenge themselves! Instead, I will write a summary of what the challenge is and my solution.

### Part 1

Given a file full of integers (one per line), find the single pair of integers that adds up to `2020`, then find the product of those two numbers.

#### Solution

[GitHub Link](https://github.com/aaronreidsmith/advent-of-code/blob/main/2020/01/raku/main.raku)

See below for explanation and any implemenation specific comments

```
sub MAIN($file) {
    say $file.IO.lines                           # [1]
          .combinations(2)                       # [2]
          .grep(-> ($a, $b) { $a + $b == 2020 }) # [3]
          .map(-> ($a, $b) { $a * $b })          # [4]
          .head;                                 # [5]
}
```

This runs as such:

```
$ raku main.raku input.txt
1020036
```

#### Explanation

This is fairly straight forward and I feel Raku reads very cleanly. Basically, we read the entire file into a list (`IO.lines`), then find all the pairs in that list, filter those pairs down to where `$a + $b == 2020`, then multiply those two numbers together!

##### Specific Comments

1. I'm a sucker for good IO. I feel reading/writing files in languages like Java or Scala is so cumbersome that I try to avoid it at all costs. Languages like Raku were _built_ for text manipultion, so it makes sense that the IO is great, but I just wanted to call out how easy it is to get the lines of a file in a list.
2. As I said in my [previous post](https://aaronreidsmith.github.io/blog/perl-weekly-challenge-089/#specific-comments), I see the `combinations` feature coming back a lot in these puzzles. I love that it is built right in.
3. `grep` is familiar to most `*nix` users, and it is the equivalent of a `filter` in more traditional functional languages. In this case, we are filtering down to only pairs that add up to `2020`.
4. At this point this list looks like this: `(($a, $b))`, so we still want to map over the outer list and multiply the pair together.
5. Since `map` returns a list, we need to grab the first item from that list for pretty printing.

### Part 2

Given the same file as before, find the _3_ numbers that add up to `2020` and find their product.

#### Solution

[GitHub Link](https://github.com/aaronreidsmith/advent-of-code/blob/main/2020/01/raku/main.raku)

See below for explanation and any implemenation specific comments

```
sub MAIN($file, Bool :$p2 = False) {                # [1]
    say $file.IO.lines
          .combinations($p2 ?? 3 !! 2)              # [2]
          .grep(-> @combo { ([+] @combo) == 2020 }) # [3]
          .map(-> @combo { [*] @combo })
          .head;
}
```

This runs as such:

```
# Part 1
$ raku main.raku input.txt
1020036

# Part 2
$ raku main.raku --p2 input.txt
286977330
```

#### Explanation

Since it is basically the same problem, it only makes sense to modify the script we have already written rather than starting from scratch. Basically, everywhere where we hardcoded `$a, $b` needs to be generalized to some list. In this case, we added a `p2` CLI flag that allows the users to specify if they are doing part 1 or part 2. If they are doing part 2 we find trios instead of pairs, then perform the same "business logic" on that collection.

##### Specific Comments

1. Using the `:$p2` notation says to Raku "create a command line flag called `--p2` and assign it to `$p2` with a default of `False`". Creating command line interfaces can be kind of a pain in a lot of languages, so I am happy that is built right into the language. 
2. This is the check to see if we are doing part 1 or part 2. Raku's ternary operator is `condition ?? true !! false` rather than the traditional `condition ? true : false`.
3. Since we have to remove all the pair hardcoding, we can generalize it as a list called `@combo` and then just find the sum of the entire combo using the `[+]` meta operator. We perform a similar generalization for the `map` step.


## Final Thoughts

So far so good with my goal to write Raku solutions functionally! Check my [GitHub](https://github.com/aaronreidsmith/advent-of-code) to see any other solutions (and any other languages, if I get around to them). This was a fun little dip into the Advent of Code, and I am looking forward to the rest of the month!